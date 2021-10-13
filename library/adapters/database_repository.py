from datetime import date
from typing import List
import math

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

    def indexes(self):
        """ Indexes property for repo. """
        raise NotImplementedError

    def dataset_of_books(self) -> List[Book]:
        """ Returns dataset of books from the repository.
        """
        raise NotImplementedError

    def books_inventory(self) -> BooksInventory:
        """ Returns a BooksInventory Object
        """
        raise NotImplementedError

    def get_book_by_id(self, book_id) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__id == book_id).one()
        except NoResultFound:
            pass # Ignore any exception and return None.

        return book

    def get_title(self, book: Book) -> str:
        return book.title

    def get_publisher(self, book: Book) -> str:
        return book.publisher

    def get_first_author(self, book: Book) -> str:
        return book.authors[0].full_name

    def get_date(self, book: Book) -> int:
        if book.release_year == None:
            return math.inf
        return book.release_year

    def get_page_by_index(self, page, text: str = None):
        """ Returns page of a book depending on the given index.
        """
        raise NotImplementedError

    def get_highest_index(self) -> int:
        """ Returns the book with highest index value in dataset of books.
        """
        raise NotImplementedError

    def first(self, page):
        """ Returns first page of book. """
        raise NotImplementedError

    def last(self, page):
        """ Returns last page of book. """
        raise NotImplementedError

    def previous(self, page):
        """ Returns previous page of book.
        """
        raise NotImplementedError

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_number_of_books(self):
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

    def add_review(self, user_name: str, book: Book, review: Review):
        user: User = self.get_user(user_name)
        if isinstance(user, User):
            user.add_review(review)
        book.add_review(review)

        # super().add_review(review)
        # with self._session_cm as scm:
        #     scm.session.add(review)
        #     scm.commit()
        