#!/usr/bin/env python3
"""Script Auth Class"""
from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
import uuid


def _hash_password(password: str) -> bytes:
    """Method hashes password and returns hash"""
    bytes_pw = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes_pw, salt)

    return hash


def _generate_uuid() -> str:
    """Method generates a unique id"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method registers a new user"""
        try:
            user_exists = self._db.find_user_by(email=email)
            if user_exists:
                raise ValueError(f"User {email} already exists")

        except NoResultFound:
            hashed_pass = _hash_password(password)
            user = self._db.add_user(email, hashed_pass)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Method validates user creds"""
        try:
            user = self._db.find_user_by(email=email)
            pass_to_bytes = password.encode("utf-8")
            return bcrypt.checkpw(pass_to_bytes, user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Method creates session id and stores it"""
        try:
            user = self._db.find_user_by(email=email)
            unique_id = _generate_uuid()
            self._db.update_user(user.id, session_id=unique_id)
            return unique_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Method gets user object from session id"""
        try:
            if session_id is None:
                return None
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Method sets session id to none"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Method generates a reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            unique_id = _generate_uuid()
            self._db.update_user(user.id, reset_token=unique_id)
            return unique_id
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Method updates user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pass = _hash_password(password)
            return self._db.update_user(user.id,
                                        hashed_password=hashed_pass,
                                        reset_token=None)
        except (NoResultFound, ValueError):
            raise ValueError
