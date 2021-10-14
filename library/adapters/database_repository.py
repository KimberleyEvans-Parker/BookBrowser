from datetime import date
from typing import List
import math

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

# from library.domain.model import User, Article, Comment, Tag
from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User
from library.adapters.repository import AbstractRepository, BOOKS_PER_PAGE


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
        self.__indexes = {"home": 0, "books_by_date": 0, "authors": 0, "publishers": 0}

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
        return self.__indexes

    def dataset_of_books(self) -> List[Book]:
        return self._session_cm.session.query(Book).all()

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
        if text is None or text.strip() == "":
            if page == "home":
                # Query to get all books, sort by first title
                books = self._session_cm.session.query(Book).order_by(Book.title.lower()).all()
            elif page == "publishers": 
                # Query to get all books, sort by publisher
                books = self._session_cm.session.query(Book).order_by(Book.publisher.name.lower()).all()
            elif page == "authors": 
                # Query to get all books, sort by first author
                books = self._session_cm.session.query(Book).order_by(Book.authors[0].lower()).all()
            else: 
                # Query to get all books, sort by date
                books = self._session_cm.session.query(Book).order_by(Book.release_year).all()
        else:
            text = text.lower().strip()
            self.indexes[page] = 0
            if page == "home":
                # Query to get all books with text in title, sort by title
                books = self._session_cm.session.query(Book).filter(text in Book.title).order_by(Book.title.lower()).all()
            elif page == "publishers":
                # Query to get all books with text in publisher, sort by publisher.name.lower
                books = self._session_cm.session.query(Book).filter(text in Book.publisher.name).order_by(Book.publisher.name.lower()).all()
            elif page == "authors":
                # Query to get all books with text in any author's name, sort by first author
                books = self._session_cm.session.query(Book).filter(text in "".join(Book.authors)).order_by(Book.authors[0].lower()).all()
            else:
                # Query to get all books with text in date, sort by first date
                books = self._session_cm.session.query(Book).filter(text in Book.release_year).order_by(Book.release_year).all()

        return books[self.__indexes[page]: self.__indexes[page] + BOOKS_PER_PAGE]

    def get_highest_index(self) -> int:
        return (math.ceil(len(self.dataset_of_books) / BOOKS_PER_PAGE) - 1) * BOOKS_PER_PAGE

    def first(self, page):
        self.__indexes[page] = 0

    def last(self, page):
        self.__indexes[page] = self.get_highest_index()

    def previous(self, page):
        self.__indexes[page] = max(0, self.__indexes[page] - BOOKS_PER_PAGE)

    def next(self, page):
        self.__indexes[page] = min(self.__indexes[page] + 12, self.get_highest_index())

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
        
