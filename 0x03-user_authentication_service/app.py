#!/usr/bin/env python3
'''A basic Flask app
'''

from flask import Flask, jsonify, make_response, redirect, request, abort
from auth import Auth


AUTH = Auth()
app = Flask('__main__')


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    ''' GET /
    Return:
      - JSON object
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    ''' POST /users
    Return:
      - Jsonified object
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    ''' POST /sessions
    Return:
      - Jsonified object
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    valid_user = AUTH.valid_login(email, password)
    print(valid_user)
    if valid_user:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response

    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    ''' DELETE /sessions
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return redirect('/')

    return make_response("", 403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    ''' GET /profile
    Return:
      - Jsonified object
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})

    return make_response("", 403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def rest_password():
    ''' POST /reset_password
    Return:
      - Jsonified object
    '''
    email = request.form.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        if reset_token:
            return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        return make_response("", 403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    ''' PUT /reset_password
    Return:
      - Jsonified object
    '''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        user = AUTH.update_password(reset_token, new_password)
        if user:
            return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        return make_response("", 403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
