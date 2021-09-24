import pytest

from flask import session
from library.domain.model import User
import library.adapters.jsondatareader as repo
from library.authentication import services
from library.authentication.services import NameNotUniqueException, UnknownUserException, AuthenticationException


@pytest.fixture()

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/register',
        data={'user_name': 'Igill', 'password': 'NissanGTR123'}
    )
    assert response.headers['Location'] == 'http://localhost/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('', 'ABCde12', b'Your user name is required'),
        ('a', '', b'Your user name is too short'),
        ('ab', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
))

def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/login').status_code
    assert status_code == 200


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session

@pytest.mark.parametrize(('review', 'messages'), (
        ('f***k this book?', (b'Your review must not contain profanity')),
        ('ass', (b'Your review must not contain profanity')),
))

def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to review on an book.
    response = client.post(
        '/review',
        data={'review': review, 'book_id': 2}
    )
    # Check that supplying invalid review text generates appropriate error messages.
    for message in messages:
        assert message in response.data

def user():
    return User('dbowie', '1234567890')

def test_user_construction():
    user1 = user()
    assert user1.user_name == 'dbowie'
    assert user1.password == '1234567890'
    assert repr(user1) == '<User dbowie>'
    assert user1.password == '1234567890'

def test_repository_can_add_a_user():
    user = User('dave', '123456789')
    services.add_user(user.user_name, user.password, repo.book_dataset)
    assert services.get_user('dave', repo.book_dataset)['user_name'] == user.user_name

def test_repository_can_retrieve_a_user():
    user = User('vegeta', '8734gfe2058v')
    services.add_user(user.user_name, user.password, repo.book_dataset)
    user = services.get_user('vegeta', repo.book_dataset)
    assert user['user_name'] == 'vegeta'

def test_repository_does_not_retrieve_a_non_existent_user():
    try:
        user = services.get_user('gohan', repo.book_dataset)
    except UnknownUserException:
        assert True

def test_can_add_user():
    new_user_name = '2jz'
    new_password = 'abcd1A23'
    services.add_user(new_user_name, new_password, repo.book_dataset)
    user_as_dict = services.get_user(new_user_name, repo.book_dataset)
    assert user_as_dict['user_name'] == new_user_name
    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name():
    user_name = 'raditz'
    password = 'Namek12345'
    services.add_user(user_name, password, repo.book_dataset)
    with pytest.raises(services.NameNotUniqueException):
        services.add_user(user_name, password, repo.book_dataset)

def test_authentication_with_valid_credentials():
    new_user_name = 'piccolo'
    new_password = 'Kami7978'
    services.add_user(new_user_name, new_password, repo.book_dataset)
    try:
        services.authenticate_user(new_user_name, new_password, repo.book_dataset)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials():
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'
    services.add_user(new_user_name, new_password, repo.book_dataset)
    try:
        services.authenticate_user(new_user_name, new_password, repo.book_dataset)
    except AuthenticationException:
        assert True


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Book browsing web application' in response.data
    assert b'Browse books by title' in response.data
    assert b'Captain America' in response.data
    assert b'Cruelle' in response.data
    assert response.data.index(b'Captain America') < response.data.index(b'Cruelle')
    assert b'Comics horror veteran Mike Wolfer writes and illustrates a powerful new chapter' in response.data
    assert b'Avatar Press' in response.data
    assert b'Yuu Asami' in response.data
    assert b'2012' in response.data
    assert b'146 pgs' in response.data
    assert b'This comes as an ebook' in response.data

def test_books_by_date(client):
    response = client.get('/books_by_date')
    assert response.status_code == 200
    assert b'Book browsing web application' in response.data
    assert b'Browse books by date' in response.data
    assert b'Superman' in response.data
    assert response.data.index(b'1997') < response.data.index(b'2006')
    assert b'These are the stories that catapulted Superman' in response.data
    assert b'DC Comics' in response.data
    assert b'Yuu Asami' in response.data
    assert b'2006' in response.data
    assert b'272 pgs' in response.data

def test_author(client):
    response = client.get('/authors')
    assert response.status_code == 200
    assert b'Book browsing web application' in response.data
    assert b'Browse books by author' in response.data
    assert b'Cruelle' in response.data
    assert response.data.index(b'Ed Brubaker') < response.data.index(b'Garth Ennis')
    assert b'The questions plaguing Captain America' in response.data
    assert b'DC Comics' in response.data
    assert b'Ed Brubaker' in response.data
    assert b'2006' in response.data
    assert b'272 pgs' in response.data

def test_publisher(client):
    response = client.get('/publishers')
    assert response.status_code == 200
    assert b'Book browsing web application' in response.data
    assert b'Browse books by publisher' in response.data
    assert b'Cruelle' in response.data
    assert response.data.index(b'Avatar Press') < response.data.index(b'Marvel')
    assert b'The questions plaguing Captain America' in response.data
    assert b'DC Comics' in response.data
    assert b'Ed Brubaker' in response.data
    assert b'2006' in response.data
    assert b'272 pgs' in response.data


def test_book(client):
    response = client.get('/book/11827783')
    assert response.status_code == 200
    assert b'Sherlock Holmes: Year One' in response.data # title
    assert b'Dynamite Entertainment' in response.data # publisher
    assert b'144' in response.data # number of pages
    assert b"Join Dr. John Watson as he meets young Sherlock Holmes in a fateful encounter" in response.data # description
    assert b'Scott Beatty' in response.data # author 1
    assert b'Daniel Indro' in response.data # author 2
    assert b'2011' in response.data # publication year
    assert b'3.16' in response.data # average rating
    assert b'114' in response.data # ratings count
    assert b'https://www.goodreads.com/book/show/11827783-sherlock-holmes' in response.data # link/url
    assert b'$5' in response.data # price
    assert b'3' in response.data # stock


# def test_login_required_to_comment(client):
#     response = client.post('/comment')
#     assert response.headers['Location'] == 'http://localhost/authentication/login'


# def test_comment(client, auth):
#     # Login a user.
#     auth.login()

#     # Check that we can retrieve the comment page.
#     response = client.get('/comment?article=2')

#     response = client.post(
#         '/comment',
#         data={'comment': 'Who needs quarantine?', 'article_id': 2}
#     )
#     assert response.headers['Location'] == 'http://localhost/articles_by_date?date=2020-02-29&view_comments_for=2'


