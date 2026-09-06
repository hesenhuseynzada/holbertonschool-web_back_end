#!/usr/bin/env python3
""" Module of Auth class
"""
from os import getenv
from typing import List, TypeVar

from flask import request


class Auth:
    """ Template for all authentication systems
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determine if a path requires authentication

        Return:
          - True if path is not in excluded_paths, False otherwise
          - the comparison is slash tolerant
          - an excluded path ending with * matches any path starting with it
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if not excluded_path.endswith('/'):
                    excluded_path += '/'
                if path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Return the value of the Authorization header of the request
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return the User instance linked to the request
        """
        return None

    def session_cookie(self, request=None):
        """ Return the value of the session cookie of the request

        The name of the cookie is defined by the environment variable
        SESSION_NAME.
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
