# poker/app/routes.py

from flask import Flask, jsonify, request, abort
from app.services import PokerGameService
import uuid

app = Flask(__name__)

# Dictionnaire pour stocker les parties avec l'ID comme clé
games = {}

def get_game(game_id):
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
    game = get_game(game_id)
    
    if not game.player_1_hand or not game.player_2_hand:
        abort(400, description="Les mains n'ont pas encore été distribuées. Commencez par distribuer les mains.")
    if len(game.community_cards) >= 3:
        abort(400, description="Le flop a déjà été distribué.")
    
    game.burn_and_deal_flop()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/turn', methods=['POST'])
def deal_turn(game_id):
    game = get_game(game_id)
    
    if len(game.community_cards) < 3:
        abort(400, description="Le flop n'a pas encore été distribué. Passez d'abord au flop.")
    if len(game.community_cards) >= 4:
        abort(400, description="Le turn a déjà été distribué.")
    
    game.burn_and_deal_turn()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/river', methods=['POST'])
def deal_river(game_id):
    game = get_game(game_id)
    
    if len(game.community_cards) < 4:
        abort(400, description="Le turn n'a pas encore été distribué. Passez d'abord au turn.")
    if len(game.community_cards) >= 5:
        abort(400, description="La river a déjà été distribuée.")
    
    game.burn_and_deal_river()
    return jsonify(game.get_game_state())

@app.route('/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    """Réinitialise une partie spécifique."""
    game = get_game(game_id)
    
    # Crée une nouvelle partie avec le même ID
    new_game = PokerGameService()
    new_game.id = game_id  # Conserve le même ID
    games[game_id] = new_game  # Remplace l'ancienne partie
    
    return jsonify({
        'message': 'La partie a été réinitialisée.',
        'game_state': new_game.get_game_state()
    })

@app.route('/<game_id>/state', methods=['GET'])
def game_state(game_id):
    game = get_game(game_id)
    return jsonify(game.get_game_state())

@app.route('/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Supprime une partie en fonction de son ID."""
    game = games.get(game_id)
    
    if not game:
        return jsonify({'message': 'Partie non trouvée.'}), 404
    
    # Supprime la partie du dictionnaire
    del games[game_id]
    
    return jsonify({'message': f'Partie {game_id} supprimée avec succès.'}), 200

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

@app.route('/games', methods=['DELETE'])
def delete_all_games():
    """Supprime toutes les parties en cours."""
    if not games:
        return jsonify({'message': 'Aucune partie en cours à supprimer.'}), 200

    games.clear()  # Supprime toutes les parties en vidant le dictionnaire.
    return jsonify({'message': 'Toutes les parties ont été supprimées.'}), 200