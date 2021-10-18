import pytest

import datetime

from sqlalchemy.exc import IntegrityError

# from covid.domain.model import User, Article, Comment, Tag, make_review, make_tag_association
from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User

book_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    new_name = "Bob"
    new_password = "Password123"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (release_year, title, description, url, ebook) VALUES '
        '(:date, "Inkheart", '
        '"Dare to read aloud...", '
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
        'true)',
        {'date': book_date.isoformat()}
    )
    row = empty_session.execute('SELECT book_id from books').fetchone()
    return row[0]


def insert_reviewed_book(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, book_id, review_text, timestamp) VALUES '
        '(:user_id, :book_id, "Review 1", :timestamp_1),'
        '(:user_id, :book_id, "Review 2", :timestamp_2)',
        {'user_id': user_key, 'book_id': book_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT book_id from books').fetchone()
    return row[0]


def make_book():
    book = Book(
        1,
        "Inkheart"
    )
    return book


def make_user():
    user = User("Bob", "111")
    return user


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Bob", "Password123"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Bob", "Password123"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Bob", None)]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Bob", "Password123"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Bob", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_book(empty_session):
    book_key = insert_book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()

    assert expected_book == fetched_book
    assert book_key == fetched_book.book_id


def test_loading_of_reviewed_book_rating(empty_session):
    insert_reviewed_book(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.rating is book.ratings_count

def test_loading_of_reviewed_book_name(empty_session):
    insert_reviewed_book(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.timestamp == book.reviews[0].timestamp


# def test_saving_of_review(empty_session):
#     book_key = insert_book(empty_session)
#     user_key = insert_user(empty_session, ("Bob", "Password123"))
#
#     rows = empty_session.query(Book).all()
#     book = rows[0]
#     user = empty_session.query(User).filter(User._User__user_name == "Bob").one()
#
#     # Create a new Review that is bidirectionally linked with the User and Book.
#     review_text = "Some review text."
#     review = Review(book.title, review_text, 5, user, 7)
#
#     # Note: if the bidirectional links between the new Review and the User and
#     # Book objects hadn't been established in memory, they would exist following
#     # committing the addition of the Review to the database.
#     empty_session.add(review)
#     empty_session.commit()
#
#     rows = list(empty_session.execute('SELECT user_id, book_id, review FROM reviews'))
#
#     assert rows == [(user_key, book_key, review_text)]


def test_saving_of_book_title(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description, release_year, ebook, num_pages, average_rating, ratings_count, url FROM books'))
    date = book_date.isoformat()
    assert rows[0][0] == book.title

def test_saving_of_book_id(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description, release_year, ebook, num_pages, average_rating, ratings_count, url FROM books'))
    date = book_date.isoformat()
    assert rows[0][1] == book.publisher

def test_saving_of_book_release(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description, release_year, ebook, num_pages, average_rating, ratings_count, url FROM books'))
    date = book_date.isoformat()
    assert rows[0][2] == book.release_year

def test_saving_of_book_ebook(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description, release_year, ebook, num_pages, average_rating, ratings_count, url FROM books'))
    date = book_date.isoformat()
    assert rows[0][3] == book.ebook

def test_saving_of_book_num_pages(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description, release_year, ebook, num_pages, average_rating, ratings_count, url FROM books'))
    date = book_date.isoformat()
    assert rows[0][4] == book.num_pages

def test_saving_of_book_ratings(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description, release_year, ebook, num_pages, average_rating, ratings_count, url FROM books'))
    date = book_date.isoformat()
    assert rows[0][5] == book.ratings_count

def test_saving_of_book_url(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description, release_year, ebook, num_pages, average_rating, ratings_count, url FROM books'))
    date = book_date.isoformat()
    assert rows[0][6] == book.url


# def test_save_reviewed_book(empty_session):
#     # Create Book User objects.
#     book = make_book()
#     user = make_user()
#
#     # Create a new Review that is bidirectionally linked with the User and Book.
#     review_text = "Some review text."
#     review = Review(book.title, review_text, 5, user, 7)
#
#     # Save the new Book.
#     empty_session.add(book)
#     empty_session.commit()
#
#     # Test test_saving_of_book() checks for insertion into the books table.
#     rows = list(empty_session.execute('SELECT book_id FROM books'))
#     book_key = rows[0][0]
#
#     # Test test_saving_of_users() checks for insertion into the users table.
#     rows = list(empty_session.execute('SELECT id FROM users'))
#     user_key = rows[0][0]
#
#     # Check that the reviews table has a new record that links to the books and users
#     # tables.
#     rows = list(empty_session.execute('SELECT user_id, book_id, review_text FROM reviews'))
#     assert rows == [(user_key, book_key, review_text)]
