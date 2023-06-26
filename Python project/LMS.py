from Book import Book

class LMS:
    def __init__(self):
        self.books = []
        self.archived_books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        return self.books.remove(book)

    def remove_book(self, index):
        return self.books.pop(index)
    
    def add_archived_book(self, book):
        self.archived_books.append(book)

    def remove_archived_book(self, book):
        return self.archived_books.remove(book)
    
    def remove_archived_book(self, index):
        return self.archived_books.pop(index)
    
    def find_book_isbn(self, isbn10, isbn13):
        for i in range(len(self.books)):
            if self.books[i].get_isbn10() == isbn10 and self.books[i].get_isbn13() == isbn13:
                return i
        return -1
        
    def find_archived_book_isbn(self, isbn10, isbn13):
        for i in range(len(self.archived_books)):
            if self.archived_books[i].get_isbn10() == isbn10 and self.archived_books[i].get_isbn13() == isbn13:
                return i
        return -1

    def get_books(self):
        return self.books
    
    def get_archived_books(self):
        return self.archived_books
    
    def set_books(self, books):
        self.books = books

    def set_archived_books(self, archived_books):
        self.archived_books = archived_books

    def __str__(self):
        result = ""
        for book in self.books:
            result += str(book) + "\n"
        return result




