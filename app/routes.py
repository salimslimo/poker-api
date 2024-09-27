# poker/app/routes.py

from flask import Flask, jsonify, request, abort
from app.services import PokerGameService
import uuid
import re
from typing import List, Dict


app = Flask(__name__)

# Regex pour valider le format UUID
UUID_REGEX = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$')

# Dictionnaire pour stocker les parties avec l'ID comme clé
games: Dict[str, PokerGameService] = {}

@app.errorhandler(400)
@app.errorhandler(404)
def custom_error_handler(error) -> Dict[str, str]:
    response = jsonify({"error": error.description})
    response.status_code = error.code
    return response

def validate_uuid(game_id: str) -> None:
    if not UUID_REGEX.match(game_id):
        abort(400, description="Invalid game_id. Format must be a UUID v4.")

def get_game(game_id: str) -> PokerGameService:
    validate_uuid(game_id)
    """Récupère une partie à partir de son ID ou renvoie une erreur 404 si elle n'existe pas."""
    game = games.get(game_id)
    if not game:
        abort(404, description="The game does not exist.")
    return game

@app.route('/start', methods=['POST'])
def start_game():
    # Génère une nouvelle partie
    num_players = request.json.get('num_players', 2)
    game = PokerGameService(num_players=num_players)
    games[game.id] = game  # Stocke la partie avec son ID

    return jsonify({
        'message': 'Partie démarrée avec succès.',
        'game_id': game.id,
        'game_state': game.get_game_state()
    })

@app.route('/<game_id>/hands', methods=['POST'])
def deal_hands(game_id: str):
    validate_uuid(game_id)
    game = get_game(game_id)
    game.deal_hands()

    return jsonify({
        'message': 'Partie démarrée avec succès.',
        'game_id': game.id,
        'game_state': game.get_game_state()
    })

@app.route('/<game_id>/flop', methods=['POST'])
def deal_flop(game_id: str):
    validate_uuid(game_id)
    game = get_game(game_id)
    game.burn_and_deal_flop()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/turn', methods=['POST'])
def deal_turn(game_id: str):
    validate_uuid(game_id)
    game = get_game(game_id)
    game.burn_and_deal_turn()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/river', methods=['POST'])
def deal_river(game_id: str):
    validate_uuid(game_id)
    game = get_game(game_id)    
    game.burn_and_deal_river()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/state', methods=['GET'])
def game_state(game_id: str):
    validate_uuid(game_id)
    game = get_game(game_id)
    return jsonify(game.get_game_state())

@app.route('/games', methods=['GET'])
def list_games():
    """Retourne la liste des parties en cours et le nombre total de parties."""
    if not games:
        return jsonify({'message': 'Aucune partie en cours.', 'number_of_games': 0}), 200

    active_games = [
        {
            'game_id': game_id,
            'player_hands': {player: [str(card) for card in hand] for player, hand in game.hands.items()},
            'community_cards': [str(card) for card in game.community_cards],
            'remaining_cards': game.deck.remaining_cards()
        }
        for game_id, game in games.items()
    ]
    
    return jsonify({'number_of_games': len(games), 'games': active_games}), 200

@app.route('/<game_id>/evaluate', methods=['GET'])
def evaluate(game_id: str):
    validate_uuid(game_id)
    game = get_game(game_id)
    return jsonify(game.evaluate()), 200