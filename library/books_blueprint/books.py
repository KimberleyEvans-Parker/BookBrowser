from flask import Blueprint, redirect, render_template, url_for

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

@books_blueprint.route('/register')
def register():
    return render_template(
        'authentication/credentials.html',
    )

@books_blueprint.route('/login')
def login():
    return render_template(
        'authentication/credentials.html',
    )

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

