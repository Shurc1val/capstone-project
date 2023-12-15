"""Module to contain and run the endpoints for the social_news API"""

from flask import Flask, current_app, request
from copy import deepcopy

app = Flask(__name__)

player_ips = []

game = {
    "state": 0,
    "number_of_players": 0,
    "counters_per_player": 0,
    "board": [[] for i in range(28)],
    "finished_tokens": []
}

players = []

@app.route("/new_game", methods=["POST"])
def new_game_endpoint():
    """
    Endpoint to start a new game on the server with the ID given in the post request; game ID
    provided must be a 5 digit integer.
    """
    global players
    global game
    
    request_dict = request.json
    
    players = request.json.get('players', [])
    players = deepcopy(players)

    game['id'] = request_dict['game']['id']
    game['state'] = 1

    game['number_of_players'] = request_dict['game']['number_of_players']
    game['counters_per_player'] = request_dict['game']['counters_per_player']
    game['board'] = deepcopy(request_dict['game']['board'])
    game['finished_tokens'] = deepcopy(request_dict['game']['finished_tokens'])
    return {}, 200


@app.route("/update", methods=["GET","POST"])
def update_endpoint():
    """
    Endpoint to either upload game details or get current status of game board from server.
    """
    global game
    global players
    global player_ips

    request_dict = request.json
    
    if request.method == "GET":
        return {
            "game": game,
            "players": players,
            "player_ips": player_ips
        }, 200

    if request.method == "POST":
        if request_dict.get('game', {}).get('id', 0) != game.get('id', 0):
            return {'error': "Invalid IP address"}, 401
        if request_dict.get('player', '') != players[0]:
            return {'error': "Not your turn"}, 401

        game['number_of_players'] = deepcopy(request_dict['game']['number_of_players'])
        game['counters_per_player'] = deepcopy(request_dict['game']['counters_per_player'])
        game['board'] = deepcopy(request_dict['game']['board'])
        game['finished_tokens'] = deepcopy(request_dict['game']['finished_tokens'])
        players = deepcopy(request_dict['players'])
        return {}, 200


@app.route("/new_player", methods=["POST"])
def new_player_endpoint():

    global game
    global player_ips
    global players

    game_id = int(request.json.get('game_id', ""))

    if game_id != game.get('id', None):
        return {
            'error': f"Invalid game id, {game_id}, {game.get('id', None)}"}, 401
    
    if game['state'] != 1:
        return {'error': "Cannot add new player in this stage of the game"}, 400

    if len(player_ips) == 5:
        return {'error': "Max player limit reached"}, 403
    
    player_ips.append(request.remote_addr)
    if len(player_ips) == len(players):
        game['state'] = 2

    return {'player': players[len(player_ips) - 1]['colour']}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
