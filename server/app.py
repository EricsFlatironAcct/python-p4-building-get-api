#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games=[]
    for game in Game.query.all():
        game_dict = create_game_dict(game)
        games.append(game_dict)

    response = make_response(
        jsonify(games),
        200,
        {"Content-Type": "application/json"} # Default return is text/html, however jsonify configures the response to json anyway so this isn't required in this case
    )
    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    game_dict = game.to_dict()

    response = make_response(
        jsonify(game_dict),
        200
    )
    return response

def create_game_dict(game):
    game_dict = {
        "title": game.title,
        "genre": game.genre,
        "platform": game.platform,
        "price": game.price
    }

    return game_dict

if __name__ == '__main__':
    app.run(port=5555, debug=True)