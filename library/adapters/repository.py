import abc
from typing import List
from datetime import date

from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User


repo_instance = None

BOOKS_PER_PAGE = 12


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
        """ Returns the highest possible page index given the number of books.
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
        
    def add_book(self, book: Book):
        """ Adds an Book to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_id(self, id: int) -> Book:
        """ Returns Book with id from the repository.

        If there is no Book with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        """ Returns the number of Books in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, user_name: str, book: Book, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with an Book and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Review not correctly attached to an Book')



    # @abc.abstractmethod
    # def get_books_by_date(self, target_date: date) -> List[Book]:
    #     """ Returns a list of Books that were published on target_date.

    #     If there are no Books on the given date, this method returns an empty list.
    #     """
    #     raise NotImplementedError
