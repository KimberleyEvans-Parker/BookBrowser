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
    Column('password', String(255), nullable=False),
    Column('reading_list', String(255)), # TODO: Should this be multiple book objects?
)

# Books and authors have a one to many relationship.
# One book can have many authors.
authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_id', ForeignKey('books.id')),
    Column('full-name', String(255), nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), nullable=False),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.id')),
    Column('rating', Integer, nullable=False),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

# One book can have multiple publishers, authors and reviews.
# Therefore book and author, review and publisher have one-to-many relationships
# as a single book object can one multiple author, review or publisher objects.
# To form this relationship we use the ForeignKey functionality.
books_table = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('publisher', String(1024)), # TODO: Should this be a publisher object?
    Column('authors', String(1024)), # TODO: Should this be multiple author objects?
    Column('release_year', Date),
    Column('ebook', Boolean),
    Column('num_pages', String(63)),
    Column('average_rating', Float),
    Column('ratings_count', Integer),
    Column('url', String(255)),
    Column('reviews', String(255)), # TODO: Should this be multiple review objects?
    Column('user_id', ForeignKey('users.id'))
)

tags_table = Table(
    'tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tag_name', String(64), nullable=False)
)

book_tags_table = Table(
    'book_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('tag_id', ForeignKey('tags.id'))
)

def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review__user')

        # '_User__reading_list:' relationship(model.Book, backref='_')
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__review': reviews_table.c.review,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(model.Book, books_table, properties={
        '_Book__id': books_table.c.id,
        '_Book__date': books_table.c.date,
        '_Book__title': books_table.c.title,
        '_Book__first_paragraph': books_table.c.first_paragraph,
        '_Book__hyperlink': books_table.c.hyperlink,
        '_Book__image_hyperlink': books_table.c.image_hyperlink,
        '_Book__reviews': relationship(model.Review, backref='_Review__book'),
        '_Book__tags': relationship(model.Tag, secondary=book_tags_table,
                                       back_populates='_Tag__tagged_books')
    })
    mapper(model.Tag, tags_table, properties={
        '_Tag__tag_name': tags_table.c.tag_name,
        '_Tag__tagged_books': relationship(
            model.Book,
            secondary=book_tags_table,
            back_populates="_Book__tags"
        )
    })