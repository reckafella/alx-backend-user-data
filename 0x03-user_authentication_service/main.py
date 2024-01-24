#!/usr/bin/env python3
'''
End-to-integration test module
'''
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    '''
    function test user registration
    '''
    user_data = {
        'email': email,
        'password': password
    }
    # First registration attempt
    response = requests.post(f'{BASE_URL}/users', data=user_data)
    # print(response.status_code)
    assert response.status_code == 200

    expected_message = {"email": f"{email}", "message": "user created"}
    assert response.json() == expected_message

    # Second attempt with same cridentials
    response = requests.post(f'{BASE_URL}/users', data=user_data)
    assert response.status_code == 400

    expected_message = {"message": "email already registered"}
    assert response.json() == expected_message


def log_in_wrong_password(email: str, password: str) -> None:
    '''
    function to test logging in with wrong password
    '''
    user_data = {
        'email': email,
        'password': password
    }
    # Login attempt with wrong password
    response = requests.post(f'{BASE_URL}/sessions', data=user_data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    '''
    function to test logging in with correct email and password
    '''
    user_data = {
        'email': email,
        'password': password
    }
    # Login attempt with correct password
    response = requests.post(f'{BASE_URL}/sessions', data=user_data)
    assert response.status_code == 200

    expected_message = {"email": f"{email}", "message": "logged in"}
    assert response.json() == expected_message
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    '''
    function test access to profile when unlogged
    '''
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    '''
    function to test access to profile when logged in
    '''
    session_cookie = {'session_id': session_id}
    response = requests.get(f'{BASE_URL}/profile', cookies=session_cookie)
    assert response.status_code == 200

    expected_message = {"email": response.json().get('email')}
    assert response.json() == expected_message


def log_out(session_id: str) -> None:
    '''
    function to test users ability to logout
    '''
    session_cookie = {'session_id': session_id}
    response = requests.delete(f'{BASE_URL}/sessions', cookies=session_cookie)
    assert response.status_code == 200

    assert response.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    '''
    function to test password reset token
    '''
    user_data = {'email': email}
    response = requests.post(f'{BASE_URL}/reset_password', data=user_data)
    assert response.status_code == 200

    reset_token = response.json().get('reset_token')
    expected_message = {'email': email, 'reset_token': reset_token}
    assert response.json() == expected_message
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''
    function to test ability to update password
    '''
    user_data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(f'{BASE_URL}/reset_password', data=user_data)
    assert response.status_code == 200

    expected_message = {"email": email, "message": "Password updated"}
    assert response.json() == expected_message


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
