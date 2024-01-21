#!/usr/bin/env python3
'''
Auth module
'''
import fnmatch
from flask import request
from typing import List, TypeVar


class Auth():
    '''
    Auth class
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        require auth method
        '''
        if not path or not excluded_paths:
            return True

        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''
        authorization header method
        '''
        if request is None:
            return None
        authorization = request.headers.get('Authorization')
        if authorization is None:
            return None
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        current user method
        '''
        return None
