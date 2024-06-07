#!/usr/bin/env python3
'''This script defines the SessionExpAuth class
'''

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''The SessionExpAuth class defined
    '''
    def __init__(self) -> None:
        '''Initilize SessionExpAuth class
        '''
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''Creates a session ID
        '''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''Returns session ID associated with sesson ID
        '''
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        sess_lifetime = created_at + timedelta(seconds=self.session_duration)

        if sess_lifetime < datetime.now():
            return None

        return session_dict.get('user_id')
