#!/usr/bin/env python3
'''
Session Authentication Module
'''
from typing import TypeVar
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    '''
    SessionAuth class
    '''
    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        '''
        creates a Session ID for a user_id
        '''
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        returns a User ID based on a Session ID
        '''
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        returns a User instance based on a cookie value
        '''
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        '''
        deletes the user session / logout
        '''
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False

        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False
        
        del self.user_id_by_session_id[session_cookie]
        return True
