from pathlib import Path

from library.adapters.csv_data_importer import load_authors_and_books, load_inventory, load_reviews, load_users

def populate(data_path: Path, repo, database_mode: bool):
    print("loading authors")
    load_authors_and_books(repo, data_path, "comic_books_excerpt.json", "book_authors_excerpt.json")
    print("loading inventory")
    load_inventory(repo, data_path, "book_inventory.json")
    print("loading users")
    load_users(repo, data_path, "users.json")
    print("loading reviews")
    load_reviews(repo, data_path, "book_reviews.csv")
