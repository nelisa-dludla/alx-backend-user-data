#!/usr/bin/env python3
'''
This module defines the BasicAuth class
'''

import base64
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth
import binascii


class BasicAuth(Auth):
    '''
    The BasicAuth class defined
    '''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''
        Returns the Base64 part of the Authorization header
        '''
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        header_parts = authorization_header.split(" ")
        return header_parts[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        Returns decode value of Base64 string
        '''
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        Returns user email and password from the Base64
        decoded value
        '''
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        header_parts = decoded_base64_authorization_header.split(":", 1)
        email, password = header_parts
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        Returns User instance
        '''
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Retrieves the User instance for a request
        '''
        authorization_header = self.authorization_header(request)
        extracted_base64_header = self.extract_base64_authorization_header(
                authorization_header)
        decoded_base64_header = self.decode_base64_authorization_header(
                extracted_base64_header)
        email, password = self.extract_user_credentials(decoded_base64_header)
        user = self.user_object_from_credentials(email, password)

        return user
