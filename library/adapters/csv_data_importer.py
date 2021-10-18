import json
import csv
from pathlib import Path
from datetime import date, datetime

from werkzeug.security import generate_password_hash

# from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def read_json_file(filename):
    lines = []
    with open(filename, encoding='UTF-8') as jsonfile:
        for line in jsonfile:
            lines.append(json.loads(line))
    return lines


def load_users(repo, data_path: Path, filename: str):
    users_json = read_json_file(data_path / filename)
    for user_item_json in users_json:
        reading_list = []
        for book_id in user_item_json["reading_list"]:
            book = repo.get_book_by_id(int(book_id))
            if book is not None:
                reading_list.append(book)
        user: User = User(user_item_json["user_name"], user_item_json["password"], reading_list)
        repo.add_user(user)


def load_reviews(repo, data_path: Path, filename: str):
    for data_row in read_csv_file(data_path / filename):
        print(data_row)
        id: int = int(data_row[0])
        user_name: str = data_row[1]
        book_id: int = int(data_row[2])
        rating: int = int(data_row[3])
        review_text: str = data_row[4]
        timestamp: str = data_row[5]

        book: Book = repo.get_book_by_id(book_id)

        review: Review = Review(book.title, review_text, rating, user_name, review_id=id, timestamp=timestamp)
        repo.add_review(user_name, book, review)


def load_authors_and_books(repo, data_path: Path, books_filename, authors_filename):
    authors_json = read_json_file(data_path / authors_filename)
    books_json = read_json_file(data_path / books_filename)

    for book_json in books_json:
        book_instance = Book(int(book_json['book_id']), book_json['title'])
        book_instance.publisher = Publisher(book_json['publisher'])
        if book_json['publication_year'] != "":
            book_instance.release_year = int(book_json['publication_year'])
        if book_json['is_ebook'].lower() == 'false':
            book_instance.ebook = False
        else:
            if book_json['is_ebook'].lower() == 'true':
                book_instance.ebook = True
        book_instance.description = book_json['description']
        if book_json['num_pages'] != "":
            book_instance.num_pages = int(book_json['num_pages'])
        book_instance.ratings_count = int(book_json["ratings_count"])
        book_instance.average_rating = float(book_json["average_rating"])
        book_instance.url = book_json["url"]

        # extract the author ids:
        list_of_authors_ids = book_json['authors']
        for author_id in list_of_authors_ids:

            numerical_id = int(author_id['author_id'])
            # We assume book authors are available in the authors file,
            # otherwise more complex handling is required.
            author_name = None
            for author_json in authors_json:
                if int(author_json['author_id']) == numerical_id:
                    author_name = author_json['name']
            book_instance.add_author(Author(numerical_id, author_name))

        repo.add_book(book_instance)


def load_inventory(repo, data_path: Path, filename):
    inventory_json = read_json_file(data_path / filename)
    for inventory_item_json in inventory_json:
        book: Book = repo.get_book_by_id(int(inventory_item_json["book_id"]))
        if book is not None:
            book_inventory: BooksInventory = repo.books_inventory
            book_inventory.add_book(book, inventory_item_json["price"], inventory_item_json["stock"])
