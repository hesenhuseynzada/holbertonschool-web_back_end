#!/usr/bin/env python3
""" Module of SessionDBAuth class
"""
from datetime import datetime, timedelta

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session authentication system with a database storage
    """

    def __init__(self):
        """ Initialize a SessionDBAuth instance

        The sessions stored on file are reloaded, so they survive a
        restart of the application.
        """
        super().__init__()
        UserSession.load_from_file()

    def create_session(self, user_id=None):
        """ Create a Session ID and store it in the database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return the User ID by requesting UserSession in the database
        """
        if session_id is None:
            return None
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if not user_sessions:
            return None
        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id
        created_at = user_session.created_at
        if created_at is None:
            return None
        expired_at = created_at + timedelta(seconds=self.session_duration)
        if expired_at < datetime.utcnow():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroy the UserSession based on the Session ID of the request
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if not user_sessions:
            return False
        user_sessions[0].remove()
        return True
