import pytest

from flask import session


# def test_register(client):
#     # Check that we retrieve the register page.
#     response_code = client.get('/authentication/register').status_code
#     assert response_code == 200

#     # Check that we can register a user successfully, supplying a valid user name and password.
#     response = client.post(
#         '/authentication/register',
#         data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
#     )
#     assert response.headers['Location'] == 'http://localhost/authentication/login'


# @pytest.mark.parametrize(('user_name', 'password', 'message'), (
#         ('', '', b'Your user name is required'),
#         ('cj', '', b'Your user name is too short'),
#         ('test', '', b'Your password is required'),
#         ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
#             a lower case letter and a digit'),
#         ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
# ))
# def test_register_with_invalid_input(client, user_name, password, message):
#     # Check that attempting to register with invalid combinations of user name and password generate appropriate error
#     # messages.
#     response = client.post(
#         '/authentication/register',
#         data={'user_name': user_name, 'password': password}
#     )
#     assert message in response.data


# def test_login(client, auth):
#     # Check that we can retrieve the login page.
#     status_code = client.get('/authentication/login').status_code
#     assert status_code == 200

#     # Check that a successful login generates a redirect to the homepage.
#     response = auth.login()
#     assert response.headers['Location'] == 'http://localhost/'

#     # Check that a session has been created for the logged-in user.
#     with client:
#         client.get('/')
#         assert session['user_name'] == 'thorke'


# def test_logout(client, auth):
#     # Login a user.
#     auth.login()

#     with client:
#         # Check that logging out clears the user's session.
#         auth.logout()
#         assert 'user_id' not in session


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Book browsing web application' in response.data
    assert b'Sherlock Holmes: Year One' in response.data
    assert b'Comics horror veteran Mike Wolfer writes and illustrates a powerful new chapter' in response.data
    assert b'DC Comics' in response.data
    assert b'Yuu Asami' in response.data
    assert b'2012' in response.data
    assert b'230 pgs' in response.data
    assert b'This comes as an ebook' in response.data


def test_book(client):
    response = client.get('/book/<11827783>')
    assert response.status_code == 200
    assert b'Sherlock Holmes: Year One' in response.data # title
    assert b'Dynamite Entertainment' in response.data # publisher
    assert b'144' in response.data # number of pages
    assert b"Sir Arthur Conan Doyle's dauntless detective returns in an all-new series of adventures exploring the \
        sleuth's untold origins! Join Dr. John Watson as he meets young Sherlock Holmes in a fateful encounter that \
        will forever shape both men's destinies! Mysteries and murders most foul abound as we discover clues that \
        reveal just how Holmes became the world's most famous detective.\nCollecting the 6-issue series in one volume, \
        plus bonus material and a complete cover gallery." in response.data # description
    assert b'Scott Beatty' in response.data # author 1
    assert b'Danie Indro' in response.data # author 2
    assert b'2011' in response.data # publication year
    assert b'3.16' in response.data # average rating
    assert b'114' in response.data # ratings count
    assert b'https://www.goodreads.com/book/show/11827783-sherlock-holmes' in response.data # link/url


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


# @pytest.mark.parametrize(('comment', 'messages'), (
#         ('Who thinks Trump is a f***wit?', (b'Your comment must not contain profanity')),
#         ('Hey', (b'Your comment is too short')),
#         ('ass', (b'Your comment is too short', b'Your comment must not contain profanity')),
# ))
# def test_comment_with_invalid_input(client, auth, comment, messages):
#     # Login a user.
#     auth.login()

#     # Attempt to comment on an article.
#     response = client.post(
#         '/comment',
#         data={'comment': comment, 'article_id': 2}
#     )
#     # Check that supplying invalid comment text generates appropriate error messages.
#     for message in messages:
#         assert message in response.data


# def test_articles_without_date(client):
#     # Check that we can retrieve the articles page.
#     response = client.get('/articles_by_date')
#     assert response.status_code == 200

#     # Check that without providing a date query parameter the page includes the first article.
#     assert b'Friday February 28 2020' in response.data
#     assert b'Coronavirus: First case of virus in New Zealand' in response.data


# def test_articles_with_date(client):
#     # Check that we can retrieve the articles page.
#     response = client.get('/articles_by_date?date=2020-02-29')
#     assert response.status_code == 200

#     # Check that all articles on the requested date are included on the page.
#     assert b'Saturday February 29 2020' in response.data
#     assert b'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary' in response.data


# def test_articles_with_comment(client):
#     # Check that we can retrieve the articles page.
#     response = client.get('/articles_by_date?date=2020-02-28&view_comments_for=1')
#     assert response.status_code == 200

#     # Check that all comments for specified article are included on the page.
#     assert b'Oh no, COVID-19 has hit New Zealand' in response.data
#     assert b'Yeah Freddie, bad news' in response.data


# def test_articles_with_tag(client):
#     # Check that we can retrieve the articles page.
#     response = client.get('/articles_by_tag?tag=Health')
#     assert response.status_code == 200

#     # Check that all articles tagged with 'Health' are included on the page.
#     assert b'Articles tagged by Health' in response.data
#     assert b'Coronavirus: First case of virus in New Zealand' in response.data
#     assert b'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary' in response.data
