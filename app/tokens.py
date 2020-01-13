from flask import jsonify, g
from app import db
from app.auth import basic_auth, token_auth
from app.api.resources import api_bp


@api_bp.route('/token/', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()

    db.session.commit()

    return jsonify({'token': token})


@api_bp.route('/token/', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()

    db.session.commit()

    return '', 204