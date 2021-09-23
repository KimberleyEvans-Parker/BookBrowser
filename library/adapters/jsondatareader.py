import json
import csv
from library.books_blueprint.books import book
from typing import List
import math

from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User

book_dataset = None

BOOKS_PER_PAGE = 12

class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str, inventory_file_name: str, reviews_file_name: str, users_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__inventory_file_name = inventory_file_name
        self.__reviews_file_name = reviews_file_name
        self.__users_file_name = users_file_name
        self.__dataset_of_books = []
        self.__books_inventory = BooksInventory()
        self.__indexes = {"home": 0, "books_by_date": 0, "authors": 0, "publishers": 0}
        self.__users = []
        self.read_json_files()

    def add_user(self, user):
        self.__users.append(user)

    def get_user(self, user_name):
        return next((user for user in self.__users if user.user_name == user_name), None)

    @property
    def indexes(self):
        return self.__indexes

    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    @property
    def books_inventory(self) -> BooksInventory:
        return self.__books_inventory

    def read_json_file(self, filename):
        lines = []
        with open(filename, encoding='UTF-8') as jsonfile:
            for line in jsonfile:
                lines.append(json.loads(line))
        return lines

    def get_book_by_id(self, book_id) -> Book:
        for book in self.__dataset_of_books:
            if book.book_id == book_id:
                return book
        return None

    def get_title(self, book: Book) -> str:
        return book.title
        
    def get_publisher(self, book: Book) -> str:
        return book.publisher

    def get_first_author(self, book: Book) -> str:
        return book.authors[0].full_name

    def get_date(self, book: Book) -> int:
        if book.release_year == None:
            return math.inf
        return book.release_year

    def get_page_by_index(self, page, text: str = None):
        if text is None:
            books = self.dataset_of_books
        elif text.strip() == "":
            text = None
            books = self.dataset_of_books
        else:
            text = text.lower().strip()

        if page == "home":
            if text is not None:
                books = [b for b in self.dataset_of_books if text in b.title.lower()]
            books.sort(key = self.get_title)
        elif page == "publishers":
            if text is not None:
                books = [b for b in self.dataset_of_books if text in b.publisher.name.lower()]
            books.sort(key = self.get_publisher)
        elif page == "authors":
            if text is not None:
                books = []
                for b in self.dataset_of_books:
                    for a in b.authors:
                        if text in a.full_name.lower():
                            books.append(b)
                            break
            books.sort(key = self.get_first_author)
        elif page == "books_by_date":
            if text is not None:
                books = [b for b in self.dataset_of_books if text in str(b.release_year)]
            books.sort(key = self.get_date)
        return books[self.__indexes[page]: self.__indexes[page] + BOOKS_PER_PAGE]

    def get_highest_index(self) -> int:
        return (math.ceil(len(self.dataset_of_books) / BOOKS_PER_PAGE) - 1) * BOOKS_PER_PAGE

    def first(self, page):
        self.__indexes[page] = 0

    def last(self, page):
        self.__indexes[page] = self.get_highest_index()

    def previous(self, page):
        self.__indexes[page] = max(0, self.__indexes[page] - BOOKS_PER_PAGE)

    def next(self, page):
        self.__indexes[page] = min(self.__indexes[page] + 12, self.get_highest_index())
        print("NEXT: new", page, " index:", self.__indexes[page])

    def read_csv_file(self, filename: str):
        with open(filename, encoding='utf-8-sig') as infile:
            reader = csv.reader(infile)

            # Read first line of the the CSV file.
            headers = next(reader)

            # Read remaining rows from the CSV file.
            for row in reader:
                # Strip any leading/trailing white space from data read.
                row = [item.strip() for item in row]
                yield row

    def read_json_files(self):
        authors_json = self.read_json_file(self.__authors_file_name)
        books_json = self.read_json_file(self.__books_file_name)
        inventory_json = self.read_json_file(self.__inventory_file_name)
        users_json = self.read_json_file(self.__users_file_name)

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

            self.__dataset_of_books.append(book_instance)

        for inventory_item_json in inventory_json:
            book:Book = self.get_book_by_id(int(inventory_item_json["book_id"]))
            if book is not None:
                self.__books_inventory.add_book(book, inventory_item_json["price"], inventory_item_json["stock"])

        for user_item_json in users_json:
            reading_list = []
            for book_id in user_item_json["reading_list"]:
                reading_list.append(self.get_book_by_id(int(book_id)))
            user:User = User(user_item_json["user_name"], user_item_json["password"], reading_list)
            self.__users.append(user)
        
        for data_row in self.read_csv_file(self.__reviews_file_name):
            id: int = int(data_row[0])
            user_name: str = data_row[1]
            book_id: int = int(data_row[2])
            rating: int = int(data_row[3])
            review_text: str = data_row[4]
            timestamp:str = data_row[5]
            
            book: Book = self.get_book_by_id(book_id)
            review: Review = Review(book_id, review_text, rating, user_name, review_id=id, timestamp=timestamp)
            book.add_review(review)




