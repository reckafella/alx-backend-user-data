#!/usr/bin/env python3
'''
Basic Authentication module
'''
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    '''
    BasicAuth class
    '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''
        Returns the Base64 part of the Authorization header for a\
            Basic Authentication
        '''
        if authorization_header is None or\
            not isinstance(authorization_header, str) or\
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        returns the decoded value of a Base64 string\
            base64_authorization_header
        '''
        if not base64_authorization_header or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decode_data = base64.b64decode(base64_authorization_header)
            return decode_data.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        returns the user email and password from the Base64 decoded value
        '''
        if not decoded_base64_authorization_header or not isinstance(
            decoded_base64_authorization_header, str) or ':' not in\
                decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        returns the User instance based on his email and password
        '''
        if not user_email or not isinstance(user_email, str) or not user_pwd\
                or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Overloads Auth and retrieves the User instance for a request:

            * use authorization_header
            * use extract_base64_authorization_header
            * use decode_base64_authorization_header
            * use extract_user_credentials
            * use user_object_from_credentials
        '''
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            authorization_header=auth_header)
        decoded_base64_header = self.decode_base64_authorization_header(
            base64_auth_header)
        u_name, u_pass = self.extract_user_credentials(decoded_base64_header)
        return self.user_object_from_credentials(u_name, u_pass)
