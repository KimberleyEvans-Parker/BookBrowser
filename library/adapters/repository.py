import abc
from typing import List
from datetime import date

from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User


repo_instance = None


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
    def add_book(self, book: Book):
        """ Adds an Book to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, id: int) -> Book:
        """ Returns Book with id from the repository.

        If there is no Book with the given id, this method returns None.
        """
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_books_by_date(self, target_date: date) -> List[Book]:
    #     """ Returns a list of Books that were published on target_date.

    #     If there are no Books on the given date, this method returns an empty list.
    #     """
    #     raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        """ Returns the number of Books in the repository. """
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_first_book(self) -> Book:
    #     """ Returns the first Book, ordered by date, from the repository.

    #     Returns None if the repository is empty.
    #     """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_last_book(self) -> Book:
    #     """ Returns the last Book, ordered by date, from the repository.

    #     Returns None if the repository is empty.
    #     """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_books_by_id(self, id_list):
    #     """ Returns a list of Books, whose ids match those in id_list, from the repository.

    #     If there are no matches, this method returns an empty list.
    #     """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_book_ids_for_tag(self, tag_name: str):
    #     """ Returns a list of ids representing Books that are tagged by tag_name.

    #     If there are no Books that are tagged by tag_name, this method returns an empty list.
    #     """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_date_of_previous_book(self, book: Book):
    #     """ Returns the date of an Book that immediately precedes book.

    #     If book is the first Book in the repository, this method returns None because there are no Books
    #     on a previous date.
    #     """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_date_of_next_book(self, book: Book):
    #     """ Returns the date of an Book that immediately follows book.

    #     If book is the last Book in the repository, this method returns None because there are no Books
    #     on a later date.
    #     """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def add_tag(self, tag: Tag):
    #     """ Adds a Tag to the repository. """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_tags(self) -> List[Tag]:
    #     """ Returns the Tags stored in the repository. """
    #     raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with an Book and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Review not correctly attached to an Book')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

