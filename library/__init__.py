"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template
from library.adapters import jsondatareader

from library.adapters.jsondatareader import BooksJSONReader

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('library') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        # data_path = app.config['TEST_DATA_PATH']

    # Initialise repo
    jsondatareader.book_dataset = BooksJSONReader(data_path/"comic_books_excerpt.json", 
        data_path/"book_authors_excerpt.json", data_path/"book_inventory.json", data_path/"reviews.json")

    jsondatareader.book_dataset.read_json_files()

    
    with app.app_context():
        from .books_blueprint import books
        app.register_blueprint(books.books_blueprint)

    return app
