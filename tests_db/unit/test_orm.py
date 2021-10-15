import pytest

import datetime

from sqlalchemy.exc import IntegrityError

# from covid.domain.model import User, Article, Comment, Tag, make_review, make_tag_association
from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User

book_date = datetime.date(2020, 2, 28)

# def insert_user(empty_session, values=None):
#     new_name = "Andrew"
#     new_password = "1234"

#     if values is not None:
#         new_name = values[0]
#         new_password = values[1]

#     empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
#                           {'user_name': new_name, 'password': new_password})
#     row = empty_session.execute('SELECT id from users where user_name = :user_name',
#                                 {'user_name': new_name}).fetchone()
#     return row[0]

# def insert_users(empty_session, values):
#     for value in values:
#         empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
#                               {'user_name': value[0], 'password': value[1]})
#     rows = list(empty_session.execute('SELECT id from users'))
#     keys = tuple(row[0] for row in rows)
#     return keys

# def insert_book(empty_session):
#     empty_session.execute(
#         'INSERT INTO books (date, title, first_paragraph, hyperlink, image_hyperlink) VALUES '
#         '(:date, "Coronavirus: First case of virus in New Zealand", '
#         '"The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.", '
#         '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
#         '"https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg")',
#         {'date': book_date.isoformat()}
#     )
#     row = empty_session.execute('SELECT id from books').fetchone()
#     return row[0]


# def insert_tags(empty_session):
#     empty_session.execute(
#         'INSERT INTO tags (tag_name) VALUES ("News"), ("New Zealand")'
#     )
#     rows = list(empty_session.execute('SELECT id from tags'))
#     keys = tuple(row[0] for row in rows)
#     return keys


# def insert_book_tag_associations(empty_session, book_key, tag_keys):
#     stmt = 'INSERT INTO book_tags (book_id, tag_id) VALUES (:book_id, :tag_id)'
#     for tag_key in tag_keys:
#         empty_session.execute(stmt, {'book_id': book_key, 'tag_id': tag_key})


# def insert_reviewed_book(empty_session):
#     book_key = insert_book(empty_session)
#     user_key = insert_user(empty_session)

#     timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     empty_session.execute(
#         'INSERT INTO reviews (user_id, book_id, review, timestamp) VALUES '
#         '(:user_id, :book_id, "Review 1", :timestamp_1),'
#         '(:user_id, :book_id, "Review 2", :timestamp_2)',
#         {'user_id': user_key, 'book_id': book_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
#     )

#     row = empty_session.execute('SELECT id from books').fetchone()
#     return row[0]


# def make_book():
#     book = Book(
#         book_date,
#         "Coronavirus: First case of virus in New Zealand",
#         "The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.",
#         "https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus",
#         "https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg"
#     )
#     return book


# def make_user():
#     user = User("Andrew", "111")
#     return user


# def make_tag():
#     tag = Tag("News")
#     return tag


# def test_loading_of_users(empty_session):
#     users = list()
#     users.append(("Andrew", "1234"))
#     users.append(("Cindy", "1111"))
#     insert_users(empty_session, users)

#     expected = [
#         User("Andrew", "1234"),
#         User("Cindy", "999")
#     ]
#     assert empty_session.query(User).all() == expected

# def test_saving_of_users(empty_session):
#     user = make_user()
#     empty_session.add(user)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT user_name, password FROM users'))
#     assert rows == [("Andrew", "111")]


# def test_saving_of_users_with_common_user_name(empty_session):
#     insert_user(empty_session, ("Andrew", "1234"))
#     empty_session.commit()

#     with pytest.raises(IntegrityError):
#         user = User("Andrew", "111")
#         empty_session.add(user)
#         empty_session.commit()


# def test_loading_of_book(empty_session):
#     book_key = insert_book(empty_session)
#     expected_book = make_book()
#     fetched_book = empty_session.query(Book).one()

#     assert expected_book == fetched_book
#     assert book_key == fetched_book.id


# def test_loading_of_tagged_book(empty_session):
#     book_key = insert_book(empty_session)
#     tag_keys = insert_tags(empty_session)
#     insert_book_tag_associations(empty_session, book_key, tag_keys)

#     book = empty_session.query(Book).get(book_key)
#     tags = [empty_session.query(Tag).get(key) for key in tag_keys]

#     for tag in tags:
#         assert book.is_tagged_by(tag)
#         assert tag.is_applied_to(book)


# def test_loading_of_reviewed_book(empty_session):
#     insert_reviewed_book(empty_session)

#     rows = empty_session.query(Book).all()
#     book = rows[0]

#     for review in book.reviews:
#         assert review.book is book


# def test_saving_of_review(empty_session):
#     book_key = insert_book(empty_session)
#     user_key = insert_user(empty_session, ("Andrew", "1234"))

#     rows = empty_session.query(Book).all()
#     book = rows[0]
#     user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

#     # Create a new Review that is bidirectionally linked with the User and Book.
#     review_text = "Some review text."
#     review = make_review(review_text, user, book)

#     # Note: if the bidirectional links between the new Review and the User and
#     # Book objects hadn't been established in memory, they would exist following
#     # committing the addition of the Review to the database.
#     empty_session.add(review)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT user_id, book_id, review FROM reviews'))

#     assert rows == [(user_key, book_key, review_text)]


# def test_saving_of_book(empty_session):
#     book = make_book()
#     empty_session.add(book)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT date, title, first_paragraph, hyperlink, image_hyperlink FROM books'))
#     date = book_date.isoformat()
#     assert rows == [(date,
#                      "Coronavirus: First case of virus in New Zealand",
#                      "The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.",
#                      "https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus",
#                      "https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg"
#                      )]


# def test_saving_tagged_book(empty_session):
#     book = make_book()
#     tag = make_tag()

#     # Establish the bidirectional relationship between the Book and the Tag.
#     make_tag_association(book, tag)

#     # Persist the Book (and Tag).
#     # Note: it doesn't matter whether we add the Tag or the Book. They are connected
#     # bidirectionally, so persisting either one will persist the other.
#     empty_session.add(book)
#     empty_session.commit()

#     # Test test_saving_of_book() checks for insertion into the books table.
#     rows = list(empty_session.execute('SELECT id FROM books'))
#     book_key = rows[0][0]

#     # Check that the tags table has a new record.
#     rows = list(empty_session.execute('SELECT id, tag_name FROM tags'))
#     tag_key = rows[0][0]
#     assert rows[0][1] == "News"

#     # Check that the book_tags table has a new record.
#     rows = list(empty_session.execute('SELECT book_id, tag_id from book_tags'))
#     book_foreign_key = rows[0][0]
#     tag_foreign_key = rows[0][1]

#     assert book_key == book_foreign_key
#     assert tag_key == tag_foreign_key


# def test_save_reviewed_book(empty_session):
#     # Create Book User objects.
#     book = make_book()
#     user = make_user()

#     # Create a new Review that is bidirectionally linked with the User and Book.
#     review_text = "Some review text."
#     review = make_review(review_text, user, book)

#     # Save the new Book.
#     empty_session.add(book)
#     empty_session.commit()

#     # Test test_saving_of_book() checks for insertion into the books table.
#     rows = list(empty_session.execute('SELECT id FROM books'))
#     book_key = rows[0][0]

#     # Test test_saving_of_users() checks for insertion into the users table.
#     rows = list(empty_session.execute('SELECT id FROM users'))
#     user_key = rows[0][0]

#     # Check that the reviews table has a new record that links to the books and users
#     # tables.
#     rows = list(empty_session.execute('SELECT user_id, book_id, review FROM reviews'))
#     assert rows == [(user_key, book_key, review_text)]
