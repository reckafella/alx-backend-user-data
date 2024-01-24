#!/usr/bin/env python3
'''
Auth Module
'''
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    '''
    method that takes in a password string arguments and returns bytes.
    '''
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)


def _generate_uuid() -> str:
    '''
    return a string representation of a new UUID using the uuid module
    '''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        takes mandatory email and password string arguments\
            and returns a User object.
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        '''
        It should expect email and password (required arguments)\
            and return a boolean.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        '''
        takes an email string argument and returns the session ID as a string.

        should find the user corresponding to the email, generate a new UUID\
            and store it in the database as the user’s session_id, then return\
                the session ID.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()

        try:
            self._db.update_user(user.id, session_id=session_id)
        except ValueError:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        '''
        takes a single session_id string argument and returns the\
            corresponding User or None.

        If the session ID is None or no user is found, return None.\
            Otherwise return the corresponding user.
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        if user.session_id is None:
            return None
        return user
