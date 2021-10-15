from sqlalchemy import select, inspect

from library.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    print()
    print(inspector.get_table_names())
    assert inspector.get_table_names() == ['authors', 'publishers', 'books', 'reviews', 'users']

# def test_database_populate_select_all_users(database_engine):

#     # Get table information
#     inspector = inspect(database_engine)
#     name_of_users_table = inspector.get_table_names()[4]

#     with database_engine.connect() as connection:
#         # query for records in table users
#         select_statement = select([metadata.tables[name_of_users_table]])
#         result = connection.execute(select_statement)

#         all_users = []
#         for row in result:
#             all_users.append(row['user_name'])

#         assert all_users == ['thorke', 'fmercury']

# def test_database_populate_select_all_reviews(database_engine):

#     # Get table information
#     inspector = inspect(database_engine)
#     name_of_reviews_table = inspector.get_table_names()[2]

#     with database_engine.connect() as connection:
#         # query for records in table reviews
#         select_statement = select([metadata.tables[name_of_reviews_table]])
#         result = connection.execute(select_statement)

#         all_reviews = []
#         for row in result:
#             all_reviews.append((row['id'], row['user_id'], row['book_id'], row['review']))

#         assert all_reviews == [(1, 2, 1, 'Oh no, COVID-19 has hit New Zealand'),
#                                 (2, 1, 1, 'Yeah Freddie, bad news')]

# def test_database_populate_select_all_books(database_engine):

#     # Get table information
#     inspector = inspect(database_engine)
#     name_of_books_table = inspector.get_table_names()[1]

#     with database_engine.connect() as connection:
#         # query for records in table books
#         select_statement = select([metadata.tables[name_of_books_table]])
#         result = connection.execute(select_statement)

#         all_books = []
#         for row in result:
#             all_books.append((row['id'], row['title']))

#         nr_books = len(all_books)
#         assert nr_books == 6

#         assert all_books[0] == (1, 'Coronavirus: First case of virus in New Zealand')


