#!/usr/bin/env python3
""" Module of BasicAuth class
"""
import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Basic authentication system
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Return the Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Return the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header,
                                       validate=True)
            return decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Return the user email and password from the decoded value

        The split is done on the first ':' only, so a password is allowed
        to contain ':' characters.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Return the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return the User instance linked to the request
        """
        authorization_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(
            authorization_header)
        decoded_header = self.decode_base64_authorization_header(
            base64_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_email, user_pwd)
