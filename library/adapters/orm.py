from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, Boolean
)
from sqlalchemy.orm import mapper, relationship, synonym
from sqlalchemy.sql.sqltypes import Float

from library.domain import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255)),
    Column('reading_list', String(255)), # TODO: Should this be multiple book objects? Yes I believe so.
)

# Books and authors have a one to many relationship.
# One book can have many authors.
authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.book_id')),   # One book has many authors but a author only has one book.
    Column('full_name', String(255), nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('book_id', ForeignKey('books.book_id'))
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), nullable=False),
    Column('user_id', ForeignKey('users.id')),  # One review has only one user but one user can have N reviews.
    Column('book_id', ForeignKey('books.book_id')), # One review belongs to a single book, but one book can have N reviews.
    Column('rating', Integer, nullable=False),
    Column('review_text', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

# One book can have multiple publishers, authors and reviews.
# Therefore book and author, review and publisher have one-to-many relationships
# as a single book object can one multiple author, review or publisher objects.
# To form this relationship we use the ForeignKey functionality.
books_table = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024)),
    # Column('publisher_id', ForeignKey('publishers.id')),
    Column('release_year', Integer),
    Column('ebook', Boolean),
    Column('num_pages', String(63)),
    Column('average_rating', Float),
    Column('ratings_count', Integer),
    Column('url', String(255)),
)

reading_list_user_table = Table(
    'reading_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.book_id')),     # This implies that a single book can have many reading lists but a readlist can only have a single book. I don't think this holds.
    Column('user_id', ForeignKey('users.id'))       # This implies that a single user can have many reading lists but a readinglist can only have a single user. I think it should be just a one to one relationship?
)

def map_model_to_tables():
    # Mappers set up the relationship between the tables and instance variables in the domain model.
    # In a one-to-many relationship such as user and review, we only define the relationship in the mapper class which holds the singularity.
    # ie one user has many reviews, hence we define the relationship in the user mapper.
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review_id')
    })
    mapper(model.Author, authors_table, properties={
        '_Author__full_name': authors_table.c.full_name
    })
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name
    })
    mapper(model.Review, reviews_table, properties={
        # '_Review__book_id': reviews_table.c.book_id, #TODO: get title rather than book
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
        # '_Review__user_name': reviews_table.c.user_name # TODO: get username rather than user?
    })
    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.book_id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__publisher': relationship(model.Publisher, backref='_Publisher_name'),
        '_Book__authors': relationship(model.Author, backref='_Author_id'),     # Was _Author__book before, don't think there is a _Author__book?
        '_Book__release_year': books_table.c.release_year,
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__average_rating': books_table.c.average_rating,
        '_Book__ratings_count': books_table.c.ratings_count,
        '_Book__url': books_table.c.url,
        '_Book__reviews': relationship(model.Review, backref='_Review_book_title'),    # There was no _Review__book instance variable in books so I made it _Review__book_title. Perhaps this will work.
        '_Book__reading_list': relationship(model.Book, secondary=reading_list_user_table)
    })
