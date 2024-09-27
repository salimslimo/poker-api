# poker/app/routes.py

from flask import Flask, jsonify, request, abort
from app.services import PokerGameService
import uuid
import re


app = Flask(__name__)

# Regex pour valider le format UUID
UUID_REGEX = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$')

# Dictionnaire pour stocker les parties avec l'ID comme clé
games = {}

@app.errorhandler(400)
@app.errorhandler(404)
def custom_error_handler(error):
    response = jsonify({"error": error.description})
    response.status_code = error.code
    return response

def validate_uuid(game_id):
    if not UUID_REGEX.match(game_id):
        abort(400, description="game_id invalide. Le format doit être un UUID v4.")

def get_game(game_id):
    validate_uuid(game_id)
    """Récupère une partie à partir de son ID ou renvoie une erreur 404 si elle n'existe pas."""
    game = games.get(game_id)
    if not game:
        abort(404, description="La partie n'existe pas.")
    return game

@app.route('/start', methods=['POST'])
def start_game():
    # Génère une nouvelle partie
    game = PokerGameService()
    games[game.id] = game  # Stocke la partie avec son ID

    # Distribue les mains aux deux joueurs
    game.deal_hands()

    return jsonify({
        'message': 'Partie démarrée avec succès.',
        'game_id': game.id,
        'game_state': game.get_game_state()
    })

@app.route('/<game_id>/flop', methods=['POST'])
def deal_flop(game_id):
    validate_uuid(game_id)
    game = get_game(game_id)
    
    if not game.player_1_hand or not game.player_2_hand:
        abort(400, description="Les mains n'ont pas encore été distribuées. Commencez par distribuer les mains.")
    if len(game.community_cards) >= 3:
        abort(400, description="Le flop a déjà été distribué.")
    
    game.burn_and_deal_flop()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/turn', methods=['POST'])
def deal_turn(game_id):
    validate_uuid(game_id)
    game = get_game(game_id)
    
    if len(game.community_cards) < 3:
        abort(400, description="Le flop n'a pas encore été distribué. Passez d'abord au flop.")
    if len(game.community_cards) >= 4:
        abort(400, description="Le turn a déjà été distribué.")
    
    game.burn_and_deal_turn()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/river', methods=['POST'])
def deal_river(game_id):
    validate_uuid(game_id)
    game = get_game(game_id)
    
    if len(game.community_cards) < 3:
        abort(400, description="Le flop n'a pas encore été distribué. Passez d'abord au flop.")
    if len(game.community_cards) < 4:
        abort(400, description="Le turn n'a pas encore été distribué. Passez d'abord au turn.")
    if len(game.community_cards) >= 5:
        abort(400, description="La river a déjà été distribuée.")
    
    game.burn_and_deal_river()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/state', methods=['GET'])
def game_state(game_id):
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
            'player_1_hand': [str(card) for card in game.player_1_hand],
            'player_2_hand': [str(card) for card in game.player_2_hand],
            'community_cards': [str(card) for card in game.community_cards],
            'remaining_cards': game.deck.remaining_cards()
        }
        for game_id, game in games.items()
    ]
    
    return jsonify({'number_of_games': len(games), 'games': active_games}), 200

@app.route('/<game_id>/evaluate', methods=['GET'])
def evaluate(game_id):
    validate_uuid(game_id)
    game = get_game(game_id)
    return jsonify(game.evaluate()), 200