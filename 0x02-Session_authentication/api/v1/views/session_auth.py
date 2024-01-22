#!/usr/bin/env python3
'''
Module for Session Authentication Views
'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_session() -> dict:
    '''
    POST /auth_session/login (= POST /api/v1/auth_session/login)
    '''
    user_email = request.form.get('email', None)
    user_pwd = request.form.get('password', None)

    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': user_email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(user_pwd):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            cookie = os.getenv('SESSION_NAME')
            response = jsonify(user.to_json())
            response.set_cookie(cookie, session_id)
            return response
        return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> dict:
    '''
    DELETE /auth_session/logout (= DELETE /api/v1/auth_session/logout)
    '''
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
