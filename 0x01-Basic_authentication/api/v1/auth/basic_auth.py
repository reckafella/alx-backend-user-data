#!/usr/bin/env python3
'''
Basic Authentication module
'''
from api.v1.auth.auth import Auth
import base64


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
