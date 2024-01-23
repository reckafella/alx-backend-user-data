#!/usr/bin/env python3
'''
Auth Module
'''
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''
    method that takes in a password string arguments and returns bytes.
    '''
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)


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
