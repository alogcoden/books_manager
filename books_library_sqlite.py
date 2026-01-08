import sqlite3 as sql

#Connection to database
connection = sql.connect("books_library.db")
print("Database was successfully created")

cursor = connection.cursor()


# cursor.execute("""
# create table library(
# id integer primary key autoincrement,
# name text not null,
# authors text not null,
# genre text,
# year integer,
# pages integer,
# read integer default 0)
# """)
# print("Table created successfully")

def book_add(name,authors,genre,year,pages):
    cursor.execute("""
    insert into library (name,authors,genre,year,pages)
        values (?,?,?,?,?)
    """, (name,authors,genre,year,pages))
    connection.commit()

# book_list = [
#     ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "Fantasy", 1997, 223),
#     ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, 310),
#     ("Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", 2011, 499),
#     ("Harry Potter and the Goblet of Fire", "J.K. Rowling", "Fantasy", 2000, 636),
#     ("Dune", "Frank Herbert", "Science Fiction", 1965, 412),
#     ("Pride and Prejudice", "Jane Austen", "Romance", 1813, 279),
#     ("War and Peace", "Leo Tolstoy", "Novel", 1869, 1225),
#     ("The Alchemist", "Paulo Coelho", "Novel", 1988, 208),
#     ("Sherlock Holmes: The Hound of the Baskervilles", "Arthur Conan Doyle", "Detective", 1902, 256),
#     ("The Kite Runner", "Khaled Hosseini", "Novel", 2003, 371)
# ]
# for book in book_list:
#     book_add(*book)

def all_books():
    cursor.execute("select * from library")
    books = cursor.fetchall()

    for i in books:
        status = "Book was read" if i[6] else "Book was not read"
        print(f"{i[0]}. {i[1]} | {i[2]} | {status}")

def was_read_books():
    cursor.execute("select name, authors from library "
                   "where read = 1")
    for i in cursor.fetchall():
        print(f"{i[0]} - {i[1]}")

def was_not_read():
    cursor.execute("select name, authors from library "
                   "where read = 0")
    for i in cursor.fetchall():
        print(f"{i[0]} - {i[1]}")

def author_book(author):
    cursor.execute(
        "select name, genre from library where authors = ?", (author,))
    for i in cursor.fetchall():
        print(f"{i[0]} - {i[1]}")

def big_book():
    cursor.execute("""
    select name, pages from library
    order by pages desc limit 1
    """)
    book = cursor.fetchone()
    if book:
        print(f"{book[0]} - {book[1]} pages ")


# Menu
try:
    while True:
        print("\nWelcome to Books Library")
        print("1. Add book")
        print("2. All books")
        print("3. Was read books")
        print("4. Was not read books")
        print("5. Search book by authors")
        print("6. Mark book as read")
        print("7. Very big book")
        print("0. Exit")

        choice = int(input("Enter your choice: "))

        # 1. Add books
        if choice == 1:
            name = input("Enter book name: ")
            authors = input("Enter book authors: ")
            genre = input("Enter book genre: ")
            year = int(input("Enter book year: "))
            pages = int(input("Enter book pages: "))
            book_add(name, authors, genre, year, pages)

        # 2. All books
        elif choice == 2:
            all_books()

        # Was read books
        elif choice == 3:
            cursor.execute("select name, authors from library where read = 1")
            books = cursor.fetchall()
            if not books:
                print("\nLibrary has no read books")
            else:
                was_read_books()

        # 3. Was not read books
        elif choice == 4:
            cursor.execute("select name from library where read = 0")
            books = cursor.fetchall()
            if not books:
                print("\nLibrary has not no read books")
            else:
                was_not_read()

        # 5. Search by authors
        elif choice == 5:
            authors = input("Enter book author: ")
            author_book(authors)

        # 6. Mark a book as read
        elif choice == 6:
            all_books()
            book_id = int(input("Enter book id: "))
            cursor.execute("update library set read = 1 where id = ?",
                           (book_id,))
            connection.commit()
            print("Book was mark")

        # 7. Very big book
        elif choice == 7:
            print("Very big book:")
            big_book()

        # Exit
        elif choice == 0:
            print("Exit")
            break

        # Invalid choice
        else:
            print("Invalid choice")

except ValueError:
    print("Enter a number!")



#Close
connection.close()
