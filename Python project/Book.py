# Book class
class Book:

    def __init__(self, title="", publisher="", isbn10="", isbn13="", optionals=None, count=1):
        self.title = title
        self.publisher = publisher
        self.isbn10 = isbn10
        self.isbn13 = isbn13
        self.optionals = optionals if optionals is not None else {}
        self.count = count

    def add_count(self):
        self.count += 1

    def add_optional(self, key, value):
        self.optionals[key] = value

    def get_optional(self, key):
        return self.optionals[key]
    
    def get_title(self):
        return self.title
    
    def get_publisher(self):
        return self.publisher
    
    def get_isbn10(self):
        return self.isbn10
    
    def get_isbn13(self):
        return self.isbn13
    
    def get_optionals(self):
        return self.optionals
    
    def get_count(self):
        return self.count
    
    def set_title(self, title):
        self.title = title

    def set_publisher(self, publisher):
        self.publisher = publisher

    def set_isbn10(self, isbn10):
        self.isbn10 = isbn10

    def set_isbn13(self, isbn13):
        self.isbn13 = isbn13

    def set_optionals(self, optionals):
        self.optionals = optionals  

    def set_count(self, count):
        self.count = count

    def __str__(self):
        return "Title: "+ self.title + "\n Publisher: " + self.publisher + "\n ISBN10: " + self.isbn10 + "\n ISBN13: " + self.isbn13 + "\n" + str(self.optionals) + "\n Count: " + str(self.count) + "\n"
    

