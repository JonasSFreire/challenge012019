import os
from flask import jsonify, request, url_for, g, abort
from . import api_bp
from app import db
from app.auth import token_auth
from app.errors import bad_request
from app.api.models.users import User


@api_bp.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message' : 'hello, world!'})


@api_bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    data = User.query.get_or_404(id).to_dict()
    return jsonify(data)


@api_bp.route('/users/', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = User.to_collection_dict(User.query, page, per_page, 'api_bp.get_users')

    return jsonify(data)


@api_bp.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    if 'id' not in data or 'email' not in data or 'password_hash' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(id=data['id']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')

    user = User()
    user.from_dict(data, new_user=True)

    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api_bp.get_user', id=user.id)

    return response


@api_bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if g.current_user.id != id:
        abort(403)

    user = User.query.get_or_404(id)

    data = request.get_json() or {}
    
    if 'id' in data and data['id'] != user.id and User.query.filter_by(id=data['id']).first():
        return bad_request('please use a different id')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first:
        return bad_request('please use a different email address')

    user.from_dict(data, new_user=False)

    db.session.commit()

    return jsonify(user.to_dict())


@api_bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    if g.current_user.id != id:
        abort(403)

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'the user has been deleted!'})