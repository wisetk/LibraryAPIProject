from sqlalchemy import create_engine, Column, String, Integer, func
from sqlalchemy.orm import sessionmaker
from data_model import Book, User, Checkout
from datetime import date
#from schemas import Book, User, Checkout # ADDED BECAUSE OF ERROR: SCHEMAS.BOOK NOT MAPPED         *IF NOT NEEDED, DELETE*
import json

# DB Location
DATABASE_URL = "sqlite:///./library.db"

# Create engine & session
engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
session = session_factory()

########### BEGIN BOOK METHODS ###########
# Get book information for all books or search by title
def get_books(name: str):
    if name:
        books = session.query(Book).filter(func.lower(Book.title) == name.lower()).all()
    else:
        books = session.query(Book).all()

    books_dict = [book.to_dict() for book in books]
    books_json = json.dumps(books_dict) 
    return books_json 

# Create new book record
def create_book(book: Book):
    new_book = Book(id=book.id, title=book.title, author=book.author, genre=book.genre, total_copies=book.total_copies, available_copies=book.available_copies)
    session.add(new_book)
    session.commit()

# Update a book record
def update_book(book: Book):
    target = session.query(Book).filter(Book.id == book.id).first()

    if target:
        target.id = book.id
        target.title = book.title
        target.author = book.author
        target.genre = book.genre
        target.total_copies = book.total_copies
        target.available_copies = book.available_copies
        session.commit()
        print(f"Record {book.id} updated.")
    else:
        print(f"Record {book.id} not found.")

# Delete book record            NEEDS TO BE TESTED
def delete_book(id: int):
    target = session.query(Book).filter(Book.id == id).first()

    if target:
        session.delete(target)
        session.commit()


########### BEGIN USER METHODS ###########
# Create new user record        NEEDS TO BE TESTED
def create_user(user: User):
    new_user = User(id=user.id, username=user.username, role=user.role)
    session.add(new_user)
    session.commit()

# Get user information for all users or a user searched by name     NEEDS TO BE TESTED
def get_user(name: str):
    if name:
        users = session.query(User).filter(func.lower(User.username) == name.lower()).all()
    else:
        users = session.query(User).all()

    users_dict = [user.to_dict() for user in users]
    users_json = json.dumps(users_dict)
    return users_json

# Update a user record          NEEDS TO BE TESTED
def update_user(user: User):
    target = session.query(User).filter(User.id == user.id).first()

    if target:
        target.id = user.id
        target.username = user.username
        target.role = user.role
        session.commit()
        print(f"User {user.id} updated.")
    else:
        print(f"User {user.id} not found.")

# Delete a user record          NEEDS TO BE TESTED
def delete_user(id: int):
    target = session.query(User).filter(User.id == id).first()

    if target:
        session.delete(target)
        session.commit()

########### BEGIN CHECKOUT METHODS ###########
# Create new checkout
def create_checkout(checkout: Checkout):
    new_checkout = Checkout(id=checkout.id, user_id=checkout.user_id, book_id=checkout.book_id, checkout_date=checkout.checkout_date, return_date=checkout.return_date)
    session.add(new_checkout)
    session.commit()

# Handle someone making a return to the library
def return_checkout(checkout_id: int):
    target = session.query(Checkout).filter(Checkout.id == checkout_id).first()
    target.return_date = date.today()

# Get checkout(s) by user ID
def get_checkout_id(user_id: int):
    print()

# Get all checkouts
def get_checkouts():
    checkouts = session.query(Checkout).all()
    checkouts_dict = [checkout.to_dict() for checkout in checkouts]
    checkouts_json = json.dumps(checkouts_dict)
    return checkouts_json