from wtforms.fields.core import IntegerField
from library.domain.model import Book, Review
from flask import Blueprint, render_template, redirect, url_for, session, request
from functools import wraps
from library.authentication import services
from library.authentication.authentication import RegistrationForm
from library.authentication.authentication import LoginForm

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

import library.adapters.jsondatareader as repo

books_blueprint = Blueprint(
    'books_bp', __name__
)

def is_left_button_inactive(function):
    if repo.book_dataset.indexes[function] == 0:
        return "disabled"
    return ""

def is_right_button_inactive(function):
    if repo.book_dataset.indexes[function] == repo.book_dataset.get_highest_index():
        return "disabled"
    return ""
    
class TextSearchForm(FlaskForm):
    text = TextAreaField("Text to find", [DataRequired()])
    submit = SubmitField("Find")

@books_blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = TextSearchForm()
    search_text = None

    if form.validate_on_submit():
        search_text = form.text.data

    return render_template(
        'home/home.html',
        title = "title",
        books = repo.book_dataset.get_page_by_index("home", search_text),
        inventory = repo.book_dataset.books_inventory,
        function = "home",
        form = form,
        left_inactive = is_left_button_inactive("home"),
        right_inactive = is_right_button_inactive("home")
    )

@books_blueprint.route('/first/<function>')
def first(function):
    repo.book_dataset.first(function)
    return redirect(url_for("books_bp." + function))

@books_blueprint.route('/previous/<function>')
def previous(function):
    repo.book_dataset.previous(function)
    return redirect(url_for("books_bp." + function))

@books_blueprint.route('/next/<function>')
def next(function):
    repo.book_dataset.next(function)
    return redirect(url_for("books_bp." + function))

@books_blueprint.route('/last/<function>')
def last(function):
    repo.book_dataset.last(function)
    return redirect(url_for("books_bp." + function))

@books_blueprint.route('/book/<id>')
def book(id):
    id = int(id)
    print(repo.book_dataset.books_inventory.find_price(id))
    print(repo.book_dataset.books_inventory.find_stock_count(id))
    return render_template(
        'books_and_reviews/book.html',
        book=repo.book_dataset.get_book_by_id(id),
        price = repo.book_dataset.books_inventory.find_price(id),
        stock = repo.book_dataset.books_inventory.find_stock_count(id)
    )

@books_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None
    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('books_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = "Your user name is already taken - please supply another"
    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('books_bp.register'),
    )

@books_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('books_bp.home'))

        except services.UnknownUserException:
            # User name not known to the system, set a suitable error message.
            user_name_not_recognised = 'User name not recognised - please supply another'

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_does_not_match_user_name = 'Password does not match supplied user name - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/credentials.html',
        title='Login',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form,
    )

@books_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('books_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('books_blueprint.login'))
        return view(**kwargs)
    return wrapped_view

@books_blueprint.route('/profile')
def profile():
    return render_template(
        'home/home.html', # TODO: create profile.html
    )

@books_blueprint.route('/reading_list')
def reading_list():
    return render_template(
        'home/home.html', # TODO: create reading_list.html
    )

@books_blueprint.route('/books_by_date')
def books_by_date():
    form = TextSearchForm()
    search_text = None

    if form.validate_on_submit():
        search_text = form.text.data

    return render_template(
        'home/home.html',
        title = "date",
        books = repo.book_dataset.get_page_by_index("books_by_date", search_text),
        inventory = repo.book_dataset.books_inventory,
        function = "books_by_date",
        form = form,
        left_inactive = is_left_button_inactive("books_by_date"),
        right_inactive = is_right_button_inactive("books_by_date")
    )

@books_blueprint.route('/authors')
def authors():
    form = TextSearchForm()
    search_text = None

    if form.validate_on_submit():
        search_text = form.text.data

    return render_template(
        'home/home.html',
        title = "author",
        books = repo.book_dataset.get_page_by_index("authors", search_text),
        inventory = repo.book_dataset.books_inventory,
        function = "authors",
        form = form,
        left_inactive = is_left_button_inactive("authors"),
        right_inactive = is_right_button_inactive("authors")
    )



@books_blueprint.route('/publishers', methods=['GET', 'POST'])
def publishers():
    form = TextSearchForm()
    search_text = None

    if form.validate_on_submit():
        search_text = form.text.data

    return render_template(
        'home/home.html',
        title = "publisher",
        books = repo.book_dataset.get_page_by_index("publishers", search_text),
        form = form,
        inventory = repo.book_dataset.books_inventory,
        function = "publishers",
        left_inactive = is_left_button_inactive("publishers"),
        right_inactive = is_right_button_inactive("publishers")
    )


# ------------------------------ Review Query Section -----------------------------


@books_blueprint.route('/write_review/<id>', methods=['GET', 'POST'])
# @login_required
def write_review(id):
    book_id = int(id) # get article id from url
    book: Book = repo.book_dataset.get_book_by_id(book_id)

    # user_name = session['user_name'] # Get uersname of person logged in

    # Create form. This maintains state, e.g. when this method is called with a HTTP GET request and populates the
    # form with an article id, when subsequently called with a HTTP POST request
    form = ReviewForm()

    if form.validate_on_submit(): # Successful POST, i.e. the comment text has passed data validation.

        review: Review = Review(book_id, form.review.data, int(form.rating.data))
        book.add_review(review)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('books_bp.book', id=book_id))

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    return render_template(
        'books_and_reviews/write_review.html',
        title='Write a Review',
        book=book,
        form=form,
        handler_url=url_for('books_bp.write_review', id=id)
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating',validators=[
        DataRequired(message="You must give an integer rating"), 
        NumberRange(min=0, max=5, message='Your rating must be between 0 and 5')])
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    submit = SubmitField('Submit')


