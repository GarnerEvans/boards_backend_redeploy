from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Board, board_schema, boards_schema

api = Blueprint('api',__name__, url_prefix='/api')



@api.route('/boards', methods = ['POST'])
@token_required
def create_board(current_user_token):
    name = request.json['name']
    length = request.json['length']
    width = request.json['width']
    wave_type = request.json['wave type']
    user_token = current_user_token.token

    board = Board(name, length, width, wave_type, user_token=user_token)

    db.session.add(board)
    db.session.commit()

    response = board_schema.dump(board)
    return jsonify(response)

@api.route('/boards', methods = ['GET'])
@token_required
def get_boards(current_user_token):
    a_user = current_user_token.token
    boards = Board.query.filter_by(user_token = a_user).all()
    response = boards_schema.dump(boards)
    return jsonify(response)

    
@api.route('/boards/<id>', methods = ['GET'])
@token_required
def get_single_board(current_user_token, id):
    board = Board.query.get(id)
    response = board_schema.dump(board)
    return jsonify(response)

@api.route('/boards/<id>', methods = ['POST','PUT'])
@token_required
def update_board(current_user_token,id):
    board = Board.query.get(id) 
    board.name = request.json['name']
    board.length = request.json['length']
    board.width = request.json['width']
    board.wave_type = request.json['wave type']
    board.user_token = current_user_token.token

    db.session.commit()
    response = board_schema.dump(board)
    return jsonify(response)

@api.route('/boards/<id>', methods = ['DELETE'])
@token_required
def delete_board(current_user_token, id):
    board = Board.query.get(id)
    db.session.delete(board)
    db.session.commit()
    response = board_schema.dump(board)
    return jsonify(response)