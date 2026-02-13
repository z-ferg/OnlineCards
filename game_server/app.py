"""
Flask backend for Gin Rummy game
Connects the Python game logic to the web interface
"""

from flask import Flask, render_template, send_from_directory, request
from game_logic import create_deck
from models import GameState
import sys
import os

app = Flask(__name__, 
            # Use the HTML, CSS, and JS in the game_client directory
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'game_client', 'static'),
            static_url_path='/static',
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'game_client', 'templates')
)

# Global game state, temporary?
game_sessions = {}

# Route the initial index call to the lobby
@app.route('/')
def index():
    return render_template('lobby.html')


# Create a new game lobby when 'Create Game' is selected from lobby
@app.route('/create', methods=['GET'])
def create_game():
    lobby_id = request.args.get('lobby_id')
    game_sessions[lobby_id] = {
        "gamestate": GameState()
    }
    game_sessions[lobby_id]["gamestate"].num_players += 1
    create_deck(game_sessions[lobby_id]["gamestate"])
    return render_template('gin_rummy.html')


# Send information that the player was able to join XYZ lobby, errors if player fails to join
#   Occurs when player inputs name in room, updates the player list of that room
@app.route('/join_game', methods=['POST'])
def join_game():
    lobby_id = request.json.get('lobby_id')
    player_name = request.json.get('player_name')
    
    if lobby_id in game_sessions:
        game_sessions[lobby_id]["gamestate"].players.append(player_name)
        print(f"Player {player_name} joined lobby {lobby_id}")
        print(game_sessions[lobby_id]["gamestate"].players)
        return {"success": True}
    else:
        return {"success": False, "error": "Lobby not found"}, 404


# Fetch the player screen when second player joins the room
#   Occurs when player hits the join button for a particular room
@app.route('/join_game', methods=['GET'])
def join_from_lobby():
    lobby_id = request.args.get('lobby_id')
    game_sessions[lobby_id]["gamestate"].num_players += 1
    return render_template('gin_rummy.html')


# Fetch all current rooms in the server, for listing on lobby screen
@app.route('/get_rooms', methods=['GET'])
def get_rooms():
    rooms = [{"lobby_id": k, "players": v["gamestate"].players, "num_players": v["gamestate"].num_players}
             for k, v in game_sessions.items()]
    return {"rooms": rooms}


# Serve assets (card images, etc.)
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    assets_folder = os.path.join(os.path.dirname(__file__), '..', 'game_client', 'assets')
    return send_from_directory(assets_folder, filename)

# Serve JavaScript files
@app.route('/js/<path:filename>')
def serve_js(filename):
    js_folder = os.path.join(os.path.dirname(__file__), '..', 'game_client', 'js')
    return send_from_directory(js_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
