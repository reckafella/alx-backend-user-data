#!/usr/bin/env python3
'''
Session Authentication Module
'''
from api.v1.auth.auth import Auth
import uuid


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
