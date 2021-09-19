from flask import Blueprint, render_template, redirect, url_for, session, request
from functools import wraps
import library.adapters.jsondatareader as repo
from A2.compsci235_assignment2_a.library.authentication import services
from A2.compsci235_assignment2_a.library.authentication.authentication import RegistrationForm
from A2.compsci235_assignment2_a.library.authentication.authentication import LoginForm

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

@books_blueprint.route('/')
def home():
    return render_template(
        'home/home.html',
        title = "Browse books by title",
        books = repo.book_dataset.get_page_by_index("home"),
        inventory = repo.book_dataset.books_inventory,
        function = "home",
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
            return redirect(url_for('home_bp.home'))

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
    return redirect(url_for('home_bp.home'))


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
    return render_template(
        'home/home.html',
        title = "Browse books by date",
        books = repo.book_dataset.get_page_by_index("books_by_date"),
        inventory = repo.book_dataset.books_inventory,
        function = "books_by_date",
        left_inactive = is_left_button_inactive("books_by_date"),
        right_inactive = is_right_button_inactive("books_by_date")
    )

@books_blueprint.route('/authors')
def authors():
    return render_template(
        'home/home.html',
        title = "Browse books by author",
        books = repo.book_dataset.get_page_by_index("authors"),
        inventory = repo.book_dataset.books_inventory,
        function = "authors",
        left_inactive = is_left_button_inactive("authors"),
        right_inactive = is_right_button_inactive("authors")
    )

@books_blueprint.route('/publishers')
def publishers():
    return render_template(
        'home/home.html',
        title = "Browse books by publisher",
        books = repo.book_dataset.get_page_by_index("publishers"),
        inventory = repo.book_dataset.books_inventory,
        function = "publishers",
        left_inactive = is_left_button_inactive("publishers"),
        right_inactive = is_right_button_inactive("publishers")
    )

