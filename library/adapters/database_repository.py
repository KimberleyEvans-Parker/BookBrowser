from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

# from library.domain.model import User, Article, Comment, Tag
from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()
        
    def get_book_by_id(self, book_id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__id == book_id).one()
        except NoResultFound:
            pass # Ignore any exception and return None.

        return book

    def get_number_of_books(self):
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books


    # def get_article_ids_for_tag(self, tag_name: str):
    #     article_ids = []

    #     # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
    #     row = self._session_cm.session.execute('SELECT id FROM tags WHERE tag_name = :tag_name', {'tag_name': tag_name}).fetchone()

    #     if row is None:
    #         # No tag with the name tag_name - create an empty list.
    #         article_ids = list()
    #     else:
    #         tag_id = row[0]
    #         # Retrieve article ids of articles associated with the tag.
    #         article_ids = self._session_cm.session.execute(
    #                 'SELECT article_id FROM article_tags WHERE tag_id = :tag_id ORDER BY article_id ASC',
    #                 {'tag_id': tag_id}
    #         ).fetchall()
    #         article_ids = [id[0] for id in article_ids]

    #     return article_ids

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()