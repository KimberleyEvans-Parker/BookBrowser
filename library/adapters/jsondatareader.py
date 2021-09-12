import json
from typing import List

from library.domain.model import BooksInventory, Publisher, Author, Book

book_dataset = None

class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str, inventory_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__inventory_file_name = inventory_file_name
        self.__dataset_of_books = []
        self.__books_inventory = BooksInventory()

    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    @property
    def books_inventory(self) -> BooksInventory:
        return self.__books_inventory

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json

    def read_inventory(self) -> list:
        inventory_json = []
        with open(self.__inventory_file_name, encoding='UTF-8') as inventory_jsonfile:
            for line in inventory_jsonfile:
                inventory_entry = json.loads(line)
                inventory_json.append(inventory_entry)
        return inventory_json

    def get_book_by_id(self, book_id) -> Book:
        for book in self.__dataset_of_books:
            if book.book_id == book_id:
                return book
        return None

    def read_json_files(self):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()
        inventory_json = self.read_inventory()

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
            print(inventory_item_json)
            book:Book = self.get_book_by_id(int(inventory_item_json["book_id"]))
            if book is not None:
                print(book)
                self.__books_inventory.add_book(book, inventory_item_json["price"], inventory_item_json["stock"])
