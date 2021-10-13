from library.books_blueprint.books import book
from typing import List
import math
from pathlib import Path

from library.domain.model import BooksInventory, Publisher, Author, Book, Review, User
from library.adapters.repository import AbstractRepository, RepositoryException

book_dataset = None

BOOKS_PER_PAGE = 12


class BooksJSONReader(AbstractRepository):
    def __init__(self, data_path: Path):
        self.__data_path = data_path
        self.__dataset_of_books = []
        self.__books_inventory = BooksInventory()
        self.__indexes = {"home": 0, "books_by_date": 0, "authors": 0, "publishers": 0}
        self.__users = []

    def add_user(self, user):
        self.__users.append(user)

    def get_user(self, user_name):
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_review(self, user_name: str, book: Book, review: Review):
        user: User = self.get_user(user_name)
        if isinstance(user, User):
            user.add_review(review)
        book.add_review(review)

    @property
    def data_path(self):
        return self.__data_path

    @property
    def data_path(self):
        return self.__data_path

    @property
    def indexes(self):
        return self.__indexes

    @property
    def users(self):
        return self.__users

    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    @property
    def books_inventory(self) -> BooksInventory:
        return self.__books_inventory

    def add_book(self, book: Book):
        self.__dataset_of_books.append(book)

    def get_number_of_books(self) -> int:
        return len(self.__dataset_of_books)

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
            self.indexes[page] = 0

        if page == "home":
            if text is not None:
                books = [b for b in self.dataset_of_books if text in b.title.lower()]
            books.sort(key=self.get_title)
        elif page == "publishers":
            if text is not None:
                books = [b for b in self.dataset_of_books if text in b.publisher.name.lower()]
            books.sort(key=self.get_publisher)
        elif page == "authors":
            if text is not None:
                books = []
                for b in self.dataset_of_books:
                    for a in b.authors:
                        if text in a.full_name.lower():
                            books.append(b)
                            break
            books.sort(key=self.get_first_author)
        elif page == "books_by_date":
            if text is not None:
                books = [b for b in self.dataset_of_books if text in str(b.release_year)]
            books.sort(key=self.get_date)
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

