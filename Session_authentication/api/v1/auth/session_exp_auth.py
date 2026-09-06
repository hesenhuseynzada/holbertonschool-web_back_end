#!/usr/bin/env python3
""" Module of SessionExpAuth class
"""
from datetime import datetime, timedelta
from os import getenv

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session authentication system with an expiration date
    """

    def __init__(self):
        """ Initialize a SessionExpAuth instance
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a Session ID and store its creation date
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return the User ID linked to a Session ID if it is not expired
        """
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None
        expired_at = created_at + timedelta(seconds=self.session_duration)
        if expired_at < datetime.now():
            return None
        return session_dictionary.get('user_id')
