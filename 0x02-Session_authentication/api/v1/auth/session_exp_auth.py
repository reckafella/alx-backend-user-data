#!/usr/bin/env python3
'''
Module to add an expiration date to a Session ID
'''
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    '''
    SessionExpAuth class
    '''
    def __init__(self):
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        '''
        method that creates a Session ID for a user_id
        '''
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        Method that returns a User ID based on Session ID
        '''
        if not session_id or session_id not in\
                self.user_id_by_session_id.keys():
            return None
        
        if 'created_at' not in self.user_id_by_session_id.keys():
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']

        if (datetime.now() - self.user_id_by_session_id[session_id]['created_at']) > timedelta(seconds=self.session_duration):
            return None
        return self.user_id_by_session_id[session_id]['user_id']
