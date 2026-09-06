#!/usr/bin/env python3
""" Module of Session authentication views
"""
from os import getenv

from flask import abort, jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Form parameters:
      - email
      - password
    Return:
      - User object JSON represented, with the Session ID as cookie
      - 400 if email or password is missing
      - 404 if no User is found for this email
      - 401 if the password is wrong
    """
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        users = []
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - an empty JSON dictionary if the session has been destroyed
      - 404 if the session can't be destroyed
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
