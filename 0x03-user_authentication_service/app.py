#!/usr/bin/env python3
'''
Basic Flask app
'''
from flask import abort, Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    '''
     return a JSON payload of the form:
        {"message": "Bienvenue"}
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    '''
    end-point to register a user
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''
    function to respond to the POST /sessions route.
    The request is expected to contain form data with\
        "email" and a "password" fields.

    If the login information is incorrect, use flask.abort to respond with a\
        401 HTTP status.

    Otherwise, create a new session for the user, store it the session ID\
        as acookie with key "session_id" on the response and\
            return a JSON payload of the form
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
