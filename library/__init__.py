"""Initialize Flask app."""

from flask import Flask, render_template
from library.adapters import jsondatareader

from library.adapters.jsondatareader import BooksJSONReader

def create_app():
    app = Flask(__name__)
    
    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')

    # Initialise repo
    jsondatareader.book_dataset = BooksJSONReader("library/adapters/data/comic_books_excerpt.json", 
        "library/adapters/data/book_authors_excerpt.json", "library/adapters/data/book_inventory.json")
    jsondatareader.book_dataset.read_json_files()
    print(len(jsondatareader.book_dataset.dataset_of_books), jsondatareader.book_dataset.dataset_of_books[0])

    
    with app.app_context():
        from .books_blueprint import books
        app.register_blueprint(books.books_blueprint)

    return app