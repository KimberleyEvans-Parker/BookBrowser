from flask import Blueprint, render_template, url_for

import library.adapters.jsondatareader as repo

books_blueprint = Blueprint(
    'books_bp', __name__
)


@books_blueprint.route('/')
def home():
    return render_template(
        'home/home.html',
        books=repo.book_dataset.dataset_of_books
    )

@books_blueprint.route('/book')
def book():
    return render_template(
        'books_and_reviews/book.html',
        book=repo.book_dataset.dataset_of_books[0] # TODO: find correct book
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

@books_blueprint.route('/books_by_date')
def books_by_date():
    return render_template(
        'home/home.html', # TODO: create books_by_date.html
    )

@books_blueprint.route('/reading_list')
def reading_list():
    return render_template(
        'home/home.html', # TODO: create reading_list.html
    )

@books_blueprint.route('/authors')
def authors():
    return render_template(
        'home/home.html', # TODO: create authors.html
    )

@books_blueprint.route('/publishers')
def publishers():
    return render_template(
        'home/home.html', # TODO: create publishers.html
    )

