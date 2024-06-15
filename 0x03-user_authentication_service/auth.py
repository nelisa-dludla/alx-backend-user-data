#!/usr/bin/env python3
"""Defines Auth class
"""

import uuid
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Returns a hashed version of argument password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    '''Returns a new uuid
    '''
    new_uuid = str(uuid.uuid4())
    return new_uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Registers the User
        '''
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        '''Checks if the user is valid
        '''
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str | None:
        '''Creates a session and returns the
        session ID
        '''
        user = self._db.find_user_by(email=email)
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id

    def get_user_from_session_id(self, session_id: str) -> User | None:
        '''Returns the User or None if not found
        '''
        user = self._db.find_user_by(session_id=session_id)
        if user:
            return User

        return None

    def destroy_session(self, user_id: int) -> None:
        '''Resets the users session ID to None
        '''
        result = self._db.update_user(user_id, session_id=None)

        return result

    def get_reset_password_token(self, email: str) -> str:
        '''Generates and returns a password reset token
        '''
        user = self._db.find_user_by(email=email)
        if user:
            reset_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

        raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''Updates the password
        '''
        user = self._db.find_user_by(reset_token=reset_token)
        if user:
            hashed_password = _hash_password(password)
            user.hashed_password = hashed_password
            user.reset_token = None
            self._db._session.commit()

        raise ValueError
