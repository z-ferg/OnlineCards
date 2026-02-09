"""
Flask backend for Gin Rummy game
Connects the Python game logic to the web interface
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
import os

# Import your game modules
from models import Card, Suit, Player, GameState
from game_logic import start_game, take_top_card, discard_card, fold
from scoring import calculate_deadwood

app = Flask(__name__, static_folder='.')
CORS(app)

# Global game state (in production, use sessions or database)
game_sessions = {}

@app.route('/')
def index():
    return send_from_directory('.', 'gin_rummy.html')

@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')

@app.route('/game.js')
def game_js():
    return send_from_directory('.', 'game.js')

@app.route('/Assets/<path:path>')
def send_asset(path):
    return send_from_directory('Assets', path)

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Start a new game"""
    data = request.json
    player_names = data.get('players', ['Player 1', 'Player 2'])
    
    players = [Player(name=name) for name in player_names]
    game_state = start_game(players)
    
    # Store game state (use session ID in production)
    session_id = 'default'
    game_sessions[session_id] = game_state
    
    return jsonify({
        'status': 'success',
        'game_state': game_state.to_dict()
    })

@app.route('/api/game_state', methods=['GET'])
def get_game_state():
    """Get current game state"""
    session_id = request.args.get('session_id', 'default')
    
    if session_id not in game_sessions:
        # Create a default game
        players = [Player(name='Katy'), Player(name='Karen')]
        game_state = start_game(players)
        game_sessions[session_id] = game_state
    
    game_state = game_sessions[session_id]
    return jsonify(game_state.to_dict())

@app.route('/api/draw', methods=['POST'])
def draw_card():
    """Draw a card from the deck"""
    session_id = request.json.get('session_id', 'default')
    
    if session_id not in game_sessions:
        return jsonify({'status': 'error', 'message': 'Game not found'}), 404
    
    game_state = game_sessions[session_id]
    card = take_top_card(game_state)
    
    if card:
        return jsonify({
            'status': 'success',
            'card': card.to_dict(),
            'game_state': game_state.to_dict()
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No cards left in deck'
        }), 400

@app.route('/api/take_discard', methods=['POST'])
def take_discard():
    """Take the top card from discard pile"""
    session_id = request.json.get('session_id', 'default')
    
    if session_id not in game_sessions:
        return jsonify({'status': 'error', 'message': 'Game not found'}), 404
    
    game_state = game_sessions[session_id]
    
    if game_state.top_card:
        current_player = game_state.players[game_state.current_turn]
        current_player.hand.append(game_state.top_card)
        taken_card = game_state.top_card
        game_state.top_card = None
        
        return jsonify({
            'status': 'success',
            'card': taken_card.to_dict(),
            'game_state': game_state.to_dict()
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No card in discard pile'
        }), 400

@app.route('/api/discard', methods=['POST'])
def discard():
    """Discard a card from hand"""
    session_id = request.json.get('session_id', 'default')
    card_data = request.json.get('card')
    
    if session_id not in game_sessions:
        return jsonify({'status': 'error', 'message': 'Game not found'}), 404
    
    game_state = game_sessions[session_id]
    current_player = game_state.players[game_state.current_turn]
    
    # Find the card in player's hand
    card_to_discard = None
    for card in current_player.hand:
        if card.rank == card_data['rank'] and card.suit.value == card_data['suit']:
            card_to_discard = card
            break
    
    if card_to_discard:
        success = discard_card(game_state, card_to_discard)
        if success:
            game_state.top_card = card_to_discard
            return jsonify({
                'status': 'success',
                'game_state': game_state.to_dict()
            })
    
    return jsonify({
        'status': 'error',
        'message': 'Card not found in hand'
    }), 400

@app.route('/api/fold', methods=['POST'])
def fold_hand():
    """Fold (knock or gin)"""
    session_id = request.json.get('session_id', 'default')
    
    if session_id not in game_sessions:
        return jsonify({'status': 'error', 'message': 'Game not found'}), 404
    
    game_state = game_sessions[session_id]
    current_player = game_state.players[game_state.current_turn]
    
    # Calculate deadwood to check if fold is valid
    deadwood = calculate_deadwood(current_player.hand)
    
    if deadwood <= 10:  # Can knock if deadwood is 10 or less
        fold(game_state)
        
        fold_type = 'Gin!' if deadwood == 0 else 'Knock'
        
        return jsonify({
            'status': 'success',
            'fold_type': fold_type,
            'deadwood': deadwood,
            'game_state': game_state.to_dict()
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'Cannot fold. Deadwood is {deadwood} (must be 10 or less)'
        }), 400

@app.route('/api/deadwood', methods=['GET'])
def get_deadwood():
    """Get deadwood count for current player"""
    session_id = request.args.get('session_id', 'default')
    
    if session_id not in game_sessions:
        return jsonify({'status': 'error', 'message': 'Game not found'}), 404
    
    game_state = game_sessions[session_id]
    current_player = game_state.players[game_state.current_turn]
    deadwood = calculate_deadwood(current_player.hand)
    
    return jsonify({
        'status': 'success',
        'deadwood': deadwood
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
