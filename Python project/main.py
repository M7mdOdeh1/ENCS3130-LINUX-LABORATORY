import os
import sys
from LMS import LMS
from Book import Book

"""
    function to lead books from a file and save it 
"""
def load_books(filename):
    books = []
    
    # open the file
    try:
        books_file = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        print("The file is not available or accessible")
    else:
        # read the file and store the books in a list
        book = Book()

        lines = books_file.readlines()
        no_of_lines = len(lines)

        i = 0
        # read the file line by line
        for line in lines:
            i+=1

            # if the line is not empty, it means that the book is not finished
            if line != "\n":
                tokens = line.split(" : ")
                # if the line is a title
                if tokens[0] == "Title":
                    book.set_title(tokens[1].strip())
                # if the line is a publisher
                elif tokens[0] == "Publisher":
                    book.set_publisher(tokens[1].strip())
                # if the line is an ISBN10
                elif tokens[0] == "ISBN10":
                    book.set_isbn10(tokens[1].strip())
                # if the line is an ISBN13
                elif tokens[0] == "ISBN13":
                    book.set_isbn13(tokens[1].strip())
                # if the line is an optional
                elif tokens[0] == "Count":
                    book.set_count(int(tokens[1].strip()))
                else:
                    book.add_optional(tokens[0].strip(), tokens[1].strip())
                
            # if the line is empty or the last line in the file, it means that the book is finished
            if line == "\n" or i == no_of_lines:
                books.append(book)
                print(book)
                book = Book()

    return books

# add books to the LMS from a file
def add_books(lms):
    
    # ask for the file name    
    filename = input("Enter file name: ")
    try:
        # open the file
        books_file = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        print("The file is not available or accessible")
    else:
        # read the file and store the books in a list
        isTitle = False
        isPublisher = False
        isISBN10 = False
        isISBN13 = False
        book = Book()

        lines = books_file.readlines()
        no_of_lines = len(lines)

        i = 0
        # read the file line by line
        for line in lines:
            i+=1 # count the number of lines

            # delete the unicode character \u200f and \u200e
            line = line.replace("\u200f", "")
            line = line.replace("\u200e", "")
            
            # if the line is not empty, it means that the book is not finished
            if line.strip() != "": 
                tokens = line.split(" : ")
                tokens[1] = tokens[1].strip()
                tokens[0] = tokens[0].strip()
                if tokens[0] == "Title":
                    book.set_title(tokens[1])
                    isTitle = True
                elif tokens[0] == "Publisher":
                    book.set_publisher(tokens[1])
                    isPublisher = True
                elif tokens[0] == "ISBN-10":
                    book.set_isbn10(tokens[1])
                    isISBN10 = True
                elif tokens[0] == "ISBN-13":
                    book.set_isbn13(tokens[1])
                    isISBN13 = True
                elif tokens[0] == "Count":
                    book.set_count(int(tokens[1]))
                else:
                    # add the optional information to the book
                    book.add_optional(tokens[0], tokens[1])

            # if the line is empty or the last line in the file, it means that the book is finished
            if line.strip() == "" or i == no_of_lines:

                # check if the book has all the basic information
                if isTitle and isPublisher and isISBN10 and isISBN13:
                    # add the book to the list
                    index = lms.find_book_isbn(book.get_isbn10(), book.get_isbn13())
                    print("--------------------------------------")
                    if index == -1:
                        print("The book has been added to the LMS.")
                        print(book)
                        lms.add_book(book)
                        
                    else:
                        print(f"The book: {book.get_title()}, with ISBN-10: {book.get_isbn10()} and ISBN-13: {book.get_isbn13()} already exists in the LMS.")
                        print("1. Replace the existing record.")
                        print("2. Add a new copy of the book.")

                        while True:
                            choice = input("Enter your choice: ")
                            if choice == "1":
                                lms.remove_book(index)
                                lms.add_book(book)
                                print("The book has been replaced!!!")
                                break
                            elif choice == "2":
                                lms.get_books()[index].add_count()
                                print("A new copy of the book has been added!!!")
                                break
                            else:
                                print("Invalid choice. Please try again.")
                                continue
                            
                        print(lms.get_books()[index])

                    print("--------------------------------------")    

                    # reset the variables
                    isTitle = False
                    isPublisher = False
                    isISBN10 = False
                    isISBN13 = False
                    book = Book()
                else:
                    print("One of the Basic information is missing (Title, Publisher, ISBN-10, ISBN-13)")
            
        # close the file
        books_file.close()


"""
Function to search for any registered book using any of the parameters (including the
optional ones) and print the results on the screen. The user should be able also to store the result in a text
file. 
"""
def search_book(lms):

    books = lms.get_books()
    # ask the user to enter the searh
    key = input ("Search for a book using any paramerter: ")
    result = []
    for book in books:
        if key == book.get_title() or key == book.get_publisher() or key == book.get_isbn10() or key == book.get_isbn13() or key in book.get_optionals().values():
            print("--------------------------------------")
            print(book)
            result.append(book)
            print("--------------------------------------")
    if len(result) == 0:
        print("No book found!!!")

    # ask the user if he wants to save the result in a file
    print("Do you want to save the result in a file?")
    print("1. Yes")
    print("2. No")
    choice = input("Enter your choice: ")
    if choice == "1":
        filename = input("Enter file name: ")
        try:
            file = open(filename, "w", encoding="utf-8")
        except FileNotFoundError:
            print("The file is not available or accessible")
        else:
            if len(result) > 0:
                for book in result:
                    file.write("--------------------------------------\n")
                    file.write(str(book))
                    file.write("--------------------------------------\n")
                print("The result has been saved in the file.")
            else:
                file.write("No book found!!!")
            file.close()


"""
When selecting this option, the LMS should prompt the user to provide the file's name or ISBN number
before letting them update the file's details. Before saving the changed data, the LMS should ask the user
for confirmation.
"""
def edit_book(lms):
    print("Edit book")
    
    # ask the user to enter the title or the ISBNs numbers to the book to be edited
    print("Enter the title or the ISBNs numbers to the book to be edited: ")
    print("1. Find the book by title")
    print("2. Find the book by ISBN-10 and ISBN-13")
    

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("Enter the title: ")
            indecies = lms.find_book_title(title)

            # if more than one book found, ask the user to choose one of them
            if len(indecies) > 1:
                print("More than one book found!!!")
                print("Please choose one of the following indecies: ")
                for i in range(len(indecies)):
                    print(f"{i+1}. {lms.get_books()[indecies[i]]}")
                index = int(input("Enter your choice: "))
                index -= 1
                
                # keep asking the user to enter a valid index
                while index < 0 or index >= len(indecies):
                    print("Invalid choice. Please try again.")
                    index = int(input("Enter your choice: "))
                    index -= 1

            elif len(indecies) == 1:
                index = 0
            else:
                print("No book found!!!")
                break

            # print the book to be edited
            print("--------------------------------------")
            print(lms.get_books()[indecies[index]])
            print("--------------------------------------")

            # ask the user to enter the new data
            print("Enter the new data (leave it blank to skip it): ")
            title = input("Enter the title: ")
            publisher = input("Enter the publisher: ")
            isbn10 = input("Enter the ISBN-10: ")
            isbn13 = input("Enter the ISBN-13: ")
            count = int(input("Enter the number of copies: "))
            optionals = {}
            for key in lms.get_books()[indecies[index]].get_optionals().keys():
                optionals[key] = input(f"Enter the {key}: ")
            
            # check if the user entered any data or leave it blank
            if title == "":
                title = lms.get_books()[indecies[index]].get_title()
            if publisher == "":
                publisher = lms.get_books()[indecies[index]].get_publisher()
            if isbn10 == "":
                isbn10 = lms.get_books()[indecies[index]].get_isbn10()
            if isbn13 == "":
                isbn13 = lms.get_books()[indecies[index]].get_isbn13()
            if count == "":
                count = lms.get_books()[indecies[index]].get_count()
            for key in optionals.keys():
                if optionals[key] == "":
                    optionals[key] = lms.get_books()[indecies[index]].get_optionals()[key]

            # create the book object
            book = Book(title, publisher, isbn10, isbn13, optionals, count)
            print("--------------------------------------")
            print(book)
            print("--------------------------------------")

            # ask the user to confirm the changes
            print("Do you want to save the changes?")
            print("1. Yes")
            print("2. No")
            choice = input("Enter your choice: ")

            while True:
                if choice == "1":
                    lms.remove_book(indecies[index])
                    lms.add_book(book)
                    print("The book has been Edited!!!")
                    break
                elif choice == "2":
                    print("The book has not been Edited!!!")
                    break
                else:
                    print("Invalid choice. Please try again.")
                    continue

            break
        elif choice == "2":
            isbn10 = input("Enter the ISBN-10: ")
            isbn13 = input("Enter the ISBN-13: ")

            # search for the book
            index = lms.find_book_isbn(isbn10, isbn13)
            if index != -1:
                # print the book to be edited
                print("--------------------------------------")
                print(lms.get_books()[index])
                print("--------------------------------------")

                # ask the user to enter the new data
                print("Enter the new data: ")
                title = input("Enter the title: ")
                publisher = input("Enter the publisher: ")
                isbn10 = input("Enter the ISBN-10: ")
                isbn13 = input("Enter the ISBN-13: ")
                count = int(input("Enter the number of copies: "))
                optionals = {}
                for key in lms.get_books()[index].get_optionals().keys():
                    optionals[key] = input(f"Enter the {key}: ")
                book = Book(title, publisher, isbn10, isbn13, optionals, count)
                print("--------------------------------------")
                print(book)
                print("--------------------------------------")

                # ask the user to confirm the changes
                print("Do you want to save the changes?")
                print("1. Yes")
                print("2. No")
                choice = input("Enter your choice: ")

                while True:
                    if choice == "1":
                        lms.remove_book(index)
                        lms.add_book(book)
                        print("The book has been Edited!!!")
                        break
                    elif choice == "2":
                        print("The book has not been Edited!!!")
                        break
                    else:
                        print("Invalid choice. Please try again.")
                        continue

            else:
                print("No book found!!!")
                break
            break
        else:
            print("Invalid choice. Please try again.")
            continue






def archive_book(lms):

    # ask the user to enter the ISBN number
    isbn10 = input("Enter the ISBN10 number: ")
    isbn13 = input("Enter the ISBN13 number: ")

    # search for the book
    index = lms.find_book_isbn(isbn10, isbn13)
    if index != -1:
        
        print("****************************************")
        print(f"The book title is: {lms.get_books()[index].get_title()}")
        # print the number of copies
        print(f"The book has {lms.get_books()[index].get_count()} copies.")

        # check if the number of copies is greater than 1
        if lms.get_books()[index].get_count() > 1:

            # ask the user how many copies he wants to archive
            count = int(input("How many copies do you want to archive?: "))

            # keep asking the user until he enters a valid number
            while count > lms.get_books()[index].get_count() or count < 0:
                print("Invalid number of copies. Please try again.")
                count = int(input("How many copies do you want to archive?: "))

            # ask the user if he really wants to archive the book
            print("Are you sure you want to archive the book?")
            print("1. Yes")
            print("2. No")
            print ("****************************************")
            choice = input("Enter your choice: ")

            while choice != "1" and choice != "2":
                print("Invalid choice. Please try again.")
                choice = input("Enter your choice: ")
            
            if choice == "1":
                # check if the number of copies is equal to the number of copies in the library
                if count == lms.get_books()[index].get_count():
                    lms.add_archived_book(lms.remove_book(index))
                    print("The book has been archived!!!")
                else:
                    # create a copy of the book with the new number of copies
                    book_copy = Book(lms.get_books()[index].get_title(), lms.get_books()[index].get_publisher(), lms.get_books()[index].get_isbn10(), lms.get_books()[index].get_isbn13(), lms.get_books()[index].get_optionals(), count)
                    # add the book to the archive
                    lms.add_archived_book(book_copy)
                    # update the number of copies in the library
                    lms.get_books()[index].set_count(lms.get_books()[index].get_count() - count)
                    
                    print("The book has been archived!!!")        
            else:
                print("The book is not archived!!!")
            
            
        else:
            # ask the user if he really wants to archive the book
            print("Are you sure you want to archive the book?")
            print("1. Yes")
            print("2. No")
            print ("****************************************")
            choice = input("Enter your choice: ")
            while choice != "1" and choice != "2":
                print("Invalid choice. Please try again.")
                choice = input("Enter your choice: ")

            if choice == "1":
                # add the book to the archive
                lms.add_archived_book(lms.remove_book(index))
                print("The book has been archived!!!")
            
            else:
                print("The book is not archived!!!")


    else:
        print("The book is not found!!!")

    

"""
Function to remove a book from the LMS. The user should be able to remove the archived books only from the LMS.
"""
def remove_book(lms):
    # ask the user to enter the ISBN number
    isbn10 = input("Enter the ISBN10 number: ")
    isbn13 = input("Enter the ISBN13 number: ")

    # search for the book
    index = lms.find_archived_book_isbn(isbn10, isbn13)

    if index != -1:
        # ask the user if he really wants to remove the book
        print("****************************************")
        print("The book title is: ", lms.get_archived_books()[index].get_title())
        print("Are you sure you want to remove the book?")
        print("1. Yes")
        print("2. No")
        print ("****************************************")
        choice = input("Enter your choice: ")
        while choice != "1" and choice != "2":
            print("Invalid choice. Please try again.")
            choice = input("Enter your choice: ")

        if choice == "1":
            # remove the book from the LMS
            lms.remove_archived_book(index)
            print("The book has been removed!!!")
        else:
            print("The book is not removed!!!")

    else:
        print("The book is not in the archived books!!!")


"""
Function to generate a report about the books include: 
1. how many books are in the LMS,
2. how many different books are offered in the LMS,3. the number of books archived in the LMS,
4. how many books in the LMS are newer than a particular year,
5. Book distribution by the publisher,
6. Books distribution by year.
"""
def generate_report(lms):
    # ask the user to enter the year
    year = int(input("Enter the year: "))
    # print the number of books in the LMS
    no_of_books = 0
    for book in lms.get_books():
        no_of_books += book.get_count()

    print(f"The number of books in the LMS is {no_of_books}.")

    # print the number of different books in the LMS
    print(f"The number of different books in the LMS is {len(lms.get_books())}.")
    
    no_of_archived_books = 0
    for book in lms.get_archived_books():
        no_of_archived_books += book.get_count()

    # print the number of books archived in the LMS
    print(f"The number of books archived in the LMS is {no_of_archived_books}.")

    no_of_books = 0
    # print the number of books in the LMS that are newer than the year entered by the user
    for book in lms.get_books():
        if 'Year' in book.get_optionals().keys():
            if int(book.get_optionals()['Year']) > year:
                no_of_books += book.get_count()
    
    if no_of_books == 0:
        print(f"There are no books in the LMS that are newer than {year}.")
    else:
        print(f"The number of books in the LMS that are newer than {year} is {no_of_books}.")

    # print the book distribution by the publisher
    publisher_distribution = {}
    for book in lms.get_books():
        if book.get_publisher() in publisher_distribution:
            publisher_distribution[book.get_publisher()] += book.get_count()
        else:
            publisher_distribution[book.get_publisher()] = book.get_count()
        
    print("The book distribution by the publisher is:")
    for publisher in publisher_distribution:
        print(f"Books From {publisher}: {publisher_distribution[publisher]}")

    # print the book distribution by the year
    year_distribution = {}
    for book in lms.get_books():
        if 'Year' in book.get_optionals().keys():
            if book.get_optionals()['Year'] in year_distribution:
                year_distribution[book.get_optionals()['Year']] += book.get_count()
            else:
                year_distribution[book.get_optionals()['Year']] = book.get_count()
        

    print("The book distribution by the year is:")
    for year in year_distribution:
        print(f"Books published in {year}: {year_distribution[year]}")

    

def exit(lms, archived_books_filename, books_filename):
    temp = ""
    # save the books in the LMS
    print("Saving the books in the LMS...")
    with open(books_filename, "w") as file:
        for book in lms.get_books():
            temp += f"ISBN10 : {book.get_isbn10()}\nISBN13 : {book.get_isbn13()}\nTitle : {book.get_title()}\nPublisher : {book.get_publisher()}\nCount : {book.get_count()}\n"
            for optional in book.get_optionals():
                temp += f"{optional} : {book.get_optionals()[optional]}\n"
        
            temp += "\n"

        # delete the last line from the file (the new line)
        temp = temp[:-2]
        file.write(temp)


    temp = ""
    # save the archived books
    print("Saving the archived books...")
    with open(archived_books_filename, "w") as file:
        for book in lms.get_archived_books():
            temp += f"ISBN10 : {book.get_isbn10()}\nISBN13 : {book.get_isbn13()}\nTitle : {book.get_title()}\nPublisher : {book.get_publisher()}\nCount : {book.get_count()}\n"
            for optional in book.get_optionals():
                temp += f"{optional} : {book.get_optionals()[optional]}\n"

            temp += "\n"
        # delete the last line from the file (the new line)
        temp = temp[:-2]
        file.write(temp)

    print("Exiting the LMS...")
    # exit the program
    sys.exit(0)




def main ():
    lms = LMS()

    # load the books in the LMS
    books_filename = "books.txt"
    archived_books_filename = "archived_books.txt"

    # check if the books file exists
    if os.path.exists(books_filename):
        print("================================================")
        print("Loading the books in the LMS...")
        lms.set_books(load_books(books_filename))
        print("The books in the LMS have been loaded successfully.")
        print("================================================")
    
    # check if the archived books file exists
    if os.path.exists(archived_books_filename):
        print("Loading the archived books...")
        lms.set_archived_books(load_books(archived_books_filename))
        print("The archived books have been loaded successfully.")
        print("================================================")


    while True:
        print("""================================================
1. Add a new books to the library collection
2. Search for a books within the library collection
3. Edit the information of an existing books
4. Archiving a book
5. Remove a book from the LMS
6. Generate a report about the books available in the LMS
7. Save and Exit
================================================""")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            add_books(lms)
        elif choice == "2":
            search_book(lms)
        elif choice == "3":
            edit_book(lms)
        elif choice == "4":
            archive_book(lms)
        elif choice == "5":
            remove_book(lms)
        elif choice == "6":
            generate_report(lms)
        elif choice == "7":
            exit(lms, archived_books_filename, books_filename)
        else:
            print("Invalid choice. Please try again.")
            continue
        




if __name__ == "__main__":
    main()