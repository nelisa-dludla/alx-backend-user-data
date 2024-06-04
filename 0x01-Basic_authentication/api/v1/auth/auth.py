#!/usr/bin/env python3
''' This module defines the auth class
'''

from typing import List, TypeVar
from flask import jsonify, request


class Auth:
    '''
    The auth class defined
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        Returns:
            - True if path not in excluded_paths
            - False if path in excluded_paths
        '''
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path.endswith("/"):
            if path in excluded_paths:
                return False
        else:
            path += "/"
            if path in excluded_paths:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        '''
        Returns the request
        '''
        if request is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Returns information on the current user
        '''
        return None
