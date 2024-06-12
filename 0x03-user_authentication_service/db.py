#!/usr/bin/env python3

"""DB module
"""
from typing import Any, Dict
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''Add a new user to DB
        '''
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        '''Find user by kwargs
        '''
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        '''Updates user by user_id and kwargs
        '''
        COLUMNS = ['id',
                   'email',
                   'hashed_password',
                   'session_id',
                   'reset_token']

        result = self._session.query(User).filter_by(id=user_id).first()
        for k, v in kwargs.items():
            if k in COLUMNS:
                setattr(result, k, v)
            else:
                raise ValueError

        self._session.commit()

        return None
