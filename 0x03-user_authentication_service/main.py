#!/usr/bin/env python3
'''Advanced Task Main
'''

import requests

BASE_URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    '''Registers a new user
    '''
    url = f'{BASE_URL}/users'
    data = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, json=data)
    assert response == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    '''Attempts to log in with incorrect password
    '''
    url = f'{BASE_URL}/sessions'
    data = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, json=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    '''Logs in
    '''
    url = f'{BASE_URL}/sessions'
    data = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, json=data)
    assert response == {"email": email, "message": "logged in"}


def profile_unlogged() -> None:
    '''Accessing profile not logged in
    '''
    url = f'{BASE_URL}/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    '''Access logged in profile
    '''
    url = f'{BASE_URL}/profile'
    data = {
        'session_id': session_id,
    }
    response = requests.get(url, cookies=data)
    assert response == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    '''Logs out
    '''
    url = f'{BASE_URL}/sessions'
    data = {
        'session_id': session_id,
    }
    response = requests.delete(url, cookies=data)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    '''Resets password
    '''
    url = f'{BASE_URL}/reset_password'
    data = {
        'email': email,
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''Updates password
    '''
    url = f'{BASE_URL}/reset_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
