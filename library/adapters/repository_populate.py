from pathlib import Path

from library.adapters.csv_data_importer import load_authors_and_books, load_inventory, load_reviews, load_users

def populate(data_path: Path, repo, database_mode: bool):
    load_users(repo, "users.json")
    load_authors_and_books(repo, "comic_books_excerpt.json", "book_authors_excerpt.json")
    load_inventory(repo, "book_inventory.json")
    load_reviews(repo, "book_reviews.csv")
