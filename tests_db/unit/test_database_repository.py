import math
from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
# from library.domain.model import User, Article, Tag, Review, make_review
from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User
from library.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('fmercury', '8734gfe2058v'))
    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_book_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_books = repo.get_number_of_books()

    assert number_of_books == 20

def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(
        1,
        "Inkheart"
    )
    repo.add_book(book)

    assert repo.get_book(book.book_id) == book


def test_repository_book_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(
        1,
        "Inkheart"
    )
    repo.add_book(book)

    assert repo.get_book_by_id(book.book_id).book_id == book.book_id


def test_repository_book_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(
        1,
        "Inkheart"
    )
    repo.add_book(book)

    assert repo.get_book_by_id(book.book_id).title == book.title


def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(
        1,
        "Inkheart"
    )
    repo.add_book(book)
    book = repo.get_book(1)

    # Check that the Book has the expected title.
    assert book.title == 'Inkheart'

def test_repository_does_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(201)
    assert book is None


def test_repository_can_retrieve_books_by_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(
        1,
        "Inkheart"
    )
    book.release_year = 2020
    books = repo.get_date(book)

    assert books == 2020


def test_repository_can_get_first_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = Book(
        1,
        "Inkheart"
    )
    repo.add_book(books)
    book = repo.get_book(books.book_id)
    assert book.title == 'Inkheart'

def can_get_number_of_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1,"Inkheart")
    book2 = Book(2, "lionheart")
    book3 = Book(3, "dogheart")
    repo.add_book(book1)
    repo.add_book(book2)
    repo.add_book(book3)
    assert repo.get_number_of_books == 3

def can_get_first_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "Inkheart")
    book1.author.append(Author(1, 'Bob Dylan'))
    book1.author.append(Author(2, 'Sideshow Bob'))
    repo.add_book(book1)
    assert repo.get_first_author(book1) == 'Bob Dylan'

def check_author_list_length(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "Inkheart")
    book1.author.append(Author(1, 'Bob Dylan'))
    book1.author.append(Author(2, 'Sideshow Bob'))
    repo.add_book(book1)
    assert repo.get_number_authors(book1) == 2

def check_can_get_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "Inkheart")
    book1.publisher = 'Kentaro Miura'
    repo.add_book(book1)
    assert repo.get_publisher == 'Kentaro Miura'


def test_repository_can_get_books_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "Inkheart")
    repo.add_book(book1)
    books = repo.get_book_by_id(1)

    assert books == book1
    assert books.title == "Inkheart"

def test_repository_does_not_retrieve_non_existent_book_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "Inkheart")
    repo.add_book(book1)
    books = repo.get_book_by_id(2)

    assert books != book1

def test_repository_returns_null_for_non_existent_book_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "Inkheart")
    repo.add_book(book1)
    books = repo.get_book_by_id(2)

    assert books is None

def test_invalid_date_returns_inf(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "Inkheart")
    repo.add_book(book1)
    assert repo.get_date(book1) == math.inf

#
#
# def test_repository_returns_date_of_previous_book(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     book = repo.get_book(6)
#     previous_date = repo.get_date_of_previous_book(book)
#
#     assert previous_date.isoformat() == '2020-03-01'
#
#
# def test_repository_returns_none_when_there_are_no_previous_books(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     book = repo.get_book(1)
#     previous_date = repo.get_date_of_previous_book(book)
#
#     assert previous_date is None
#
#
# def test_repository_returns_date_of_next_book(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     book = repo.get_book(3)
#     next_date = repo.get_date_of_next_book(book)
#
#     assert next_date.isoformat() == '2020-03-05'
#
#
# def test_repository_returns_none_when_there_are_no_subsequent_books(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     book = repo.get_book(177)
#     next_date = repo.get_date_of_next_book(book)
#
#     assert next_date is None
#
#
# def test_repository_can_add_a_review(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     user = repo.get_user('thorke')
#     book = repo.get_book(2)
#     review_text = "Some review text."
#     review = Review(book.title, review_text, 5, user, 7)
#     repo.add_book(book)
#     book.reviews.append(review)
#     repo.add_review(review)
#
#     assert review in repo.get_reviews()
#
#
# def test_repository_does_not_add_a_review_without_a_user(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     book = repo.get_book(2)
#     review = Review(None, book, "Trump's onto it!", datetime.today())
#
#     with pytest.raises(RepositoryException):
#         repo.add_review(review)
#
#
# def test_repository_can_retrieve_reviews(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     assert len(repo.get_reviews()) == 3
#
#
# def make_book(new_book_date):
#     book1 = Book(1, "Inkheart")
#     return book1
#
# def test_can_retrieve_an_book_and_add_a_review_to_it(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#
#     # Fetch Book and User.
#     book = repo.get_book(5)
#     author = repo.get_user('thorke')
#
#     # Create a new Review, connecting it to the Book and User.
#     review = make_review('First death in Australia', author, book)
#
#     book_fetched = repo.get_book(5)
#     author_fetched = repo.get_user('thorke')
#
#     assert review in book_fetched.reviews
#     assert review in author_fetched.reviews

