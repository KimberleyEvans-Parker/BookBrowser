from flask import Blueprint, redirect, render_template, url_for

import library.adapters.jsondatareader as repo

books_blueprint = Blueprint(
    'books_bp', __name__
)

@books_blueprint.route('/')
def home():
    left_inactive = ""
    right_inactive = ""

    if repo.book_dataset.indexes["home"] == 0:
        left_inactive = "disabled"
    if repo.book_dataset.indexes["home"] == repo.book_dataset.get_highest_index():
        right_inactive = "disabled"

    return render_template(
        'home/home.html',
        books = repo.book_dataset.get_page_by_index("home"),
        inventory = repo.book_dataset.books_inventory,
        function = "home",
        left_inactive = left_inactive,
        right_inactive = right_inactive
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
    left_inactive = ""
    right_inactive = ""

    if repo.book_dataset.indexes["books_by_date"] == 0:
        left_inactive = "disabled"
    if repo.book_dataset.indexes["books_by_date"] == repo.book_dataset.get_highest_index():
        right_inactive = "disabled"

    return render_template(
        'home/home.html',
        books = repo.book_dataset.get_page_by_index("books_by_date"),
        inventory = repo.book_dataset.books_inventory,
        function = "books_by_date",
        left_inactive = left_inactive,
        right_inactive = right_inactive
    )

@books_blueprint.route('/authors')
def authors():
    left_inactive = ""
    right_inactive = ""

    if repo.book_dataset.indexes["authors"] == 0:
        left_inactive = "disabled"
    if repo.book_dataset.indexes["authors"] == repo.book_dataset.get_highest_index():
        right_inactive = "disabled"

    return render_template(
        'home/home.html',
        books = repo.book_dataset.get_page_by_index("authors"),
        inventory = repo.book_dataset.books_inventory,
        function = "authors",
        left_inactive = left_inactive,
        right_inactive = right_inactive
    )

@books_blueprint.route('/publishers')
def publishers():
    left_inactive = ""
    right_inactive = ""

    if repo.book_dataset.indexes["publishers"] == 0:
        left_inactive = "disabled"
    if repo.book_dataset.indexes["publishers"] == repo.book_dataset.get_highest_index():
        right_inactive = "disabled"

    return render_template(
        'home/home.html',
        books = repo.book_dataset.get_page_by_index("publishers"),
        inventory = repo.book_dataset.books_inventory,
        function = "publishers",
        left_inactive = left_inactive,
        right_inactive = right_inactive
    )

