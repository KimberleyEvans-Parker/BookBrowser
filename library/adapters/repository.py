import abc
from typing import List

from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def indexes(self):
        """ Indexes property for repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def dataset_of_books(self) -> List[Book]:
        """ Returns dataset of books from the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def books_inventory(self) -> BooksInventory:
        """ Returns a BooksInventory Object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_id(self, book_id) -> Book:
        """ Returns Book object which has matching id.

         If there is no such Book returns None.
         """
        raise NotImplementedError

    @abc.abstractmethod
    def get_title(self, book: Book) -> str:
        """ Returns String depicting title of a given Book object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher(self, book: Book) -> str:
        """ Returns the publisher of a given Book object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_author(self, book: Book) -> str:
        """ Returns the first author in a possible list of many authors for a given Book object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date(self, book: Book) -> int:
        """ Returns the release date of a given Book object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_page_by_index(self, page, text: str = None):
        """ Returns page of a book depending on the given index.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_highest_index(self) -> int:
        """ Returns the book with highest index value in dataset of books.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def first(self, page):
        """ Returns first page of book. """
        raise NotImplementedError

    @abc.abstractmethod
    def last(self, page):
        """ Returns last page of book. """
        raise NotImplementedError

    @abc.abstractmethod
    def previous(self, page):
        """ Returns previous page of book.
        """
        raise NotImplementedError
