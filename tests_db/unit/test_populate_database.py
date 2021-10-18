from sqlalchemy import select, inspect

from library.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'authors_books', 'books', 'publishers', 'reading_list', 'reviews', 'users']

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[-1]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['John Smith', 'Peter Parker', 'Klark Kent', 'Matilda', 'Belle', 'Hermione Granger', 'The Doctor', 'Goku']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[-2]

    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['id'], row['user_id'], row['book_id'], row['rating'], row['review_text']))

        assert (10, 3, 707611, 1, 'Just not realistic') in all_reviews
        assert (13, 1, 11827783, 5, 'One of the best detective novels of all time.') in all_reviews
        assert (7, 7, 27036539, 5, 'This book had me crying.  Heart-breaking and informative') in all_reviews
        assert len(all_reviews) == 39

def test_database_populate_select_all_books(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_books_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table books
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['book_id'], row['title']))

        assert (707611, 'Superman Archives, Vol. 2') in all_books
        assert (35452242, 'Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC') in all_books
        assert (11827783, 'Sherlock Holmes: Year One') in all_books
        assert len(all_books) == 20

def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_books_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table books
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append((row['name']))

        assert 'Marvel' in all_publishers
        assert 'Dynamite Entertainment' in all_publishers
        assert 'Avatar Press' in all_publishers
        assert len(all_publishers) == 20

def test_database_populate_select_all_authors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_books_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table books
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)

        all_authors = []
        for row in result:
            all_authors.append((row['full_name']))

        assert 'Jaymes Reed' in all_authors
        assert 'Garth Ennis' in all_authors
        assert 'Chris  Martin' in all_authors
        assert len(all_authors) == 35
