"""
Flask backend for Gin Rummy game
Connects the Python game logic to the web interface
"""

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import sys
import os

app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'game_client', 'static'),
            static_url_path='/static',
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'game_client', 'templates')
)

# Global game state (in production, use sessions or database)
game_sessions = {}

# Route lobby page as index
@app.route('/')
def index():
    return render_template('lobby.html')

# Route creating a new game
@app.route('/create')
def create_game():
    return render_template('gin_rummy.html')

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
