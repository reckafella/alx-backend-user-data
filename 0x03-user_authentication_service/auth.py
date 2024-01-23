#!/usr/bin/env python3
'''
Auth Module
'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''
    method that takes in a password string arguments and returns bytes.
    '''
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)
