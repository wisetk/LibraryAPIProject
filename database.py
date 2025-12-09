from sqlalchemy import create_engine, Column, String, Integer, func
from sqlalchemy.orm import sessionmaker
from data_model import Book, User, Checkout
from schemas import CheckoutCreate
from datetime import date
import json

# DB Location
DATABASE_URL = "sqlite:///./library.db"

# Create engine & session
engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
session = session_factory()

########### BEGIN BOOK METHODS ###########
# Get a unique value to assign as the book's ID
def get_unique_book_id():
    books = session.query(Book).all()
    new_id = len(books) + 1
    return new_id

# Get book information for all books 
def get_books():
    books = session.query(Book).all()
    books_dict = [book.to_dict() for book in books]
    return books_dict

# Get book information based on a title search query
def get_books_by_title(title: str):
    books = session.query(Book).filter(Book.title.like(f"%{title}%")).all()
    books_dict = [book.to_dict() for book in books]
    return books_dict

# Get a specific book record by searching ID
def get_book_by_id(book_id: int):
    book = session.query(Book).filter(Book.id == book_id).first()
    return book.to_dict()

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

# Delete book record
def delete_book(id: int):
    target = session.query(Book).filter(Book.id == id).first()

    if target:
        session.delete(target)
        session.commit()


########### BEGIN USER METHODS ###########
# Get unique user ID
def get_unique_user_id():
    users = session.query(User).all()
    new_id = len(users) + 1
    return new_id

# Create new user record
def create_user(user: User):
    new_user = User(id=user.id, username=user.username, role=user.role)
    session.add(new_user)
    session.commit()

# Get user information for all users
def get_users():
    users = session.query(User).all()
    users_dict = [user.to_dict() for user in users]
    return users_dict

# Get user information by searching for username
def get_users_by_username(name: str):
    users = session.query(User).filter(User.username.like(f"%{name}%")).all()
    users_dict = [user.to_dict() for user in users]
    return users_dict

# Get user information by searching the user ID
def get_user_by_id(id: int):
    user = session.query(User).filter(User.id == id).first()
    return user.to_dict()

# Update a user record
def update_user(user: User):
    target = session.query(User).filter(User.id == user.id).first()

    if target:
        target.id = user.id
        target.username = user.username
        target.role = user.role
        session.commit()
        print(f"User number {user.id} updated.")
    else:
        print(f"User number {user.id} not found.")

# Delete a user record
def delete_user(id: int):
    target = session.query(User).filter(User.id == id).first()

    if target:
        session.delete(target)
        session.commit()

########### BEGIN CHECKOUT METHODS ###########
# Get unique checkout ID
def get_unique_checkout_id():
    checkouts = session.query(Checkout).all()
    new_id = len(checkouts) + 1
    return new_id

# Create new checkout
def create_checkout(checkout: CheckoutCreate):
    new_checkout = Checkout(user_id=checkout.user_id, book_id=checkout.book_id, checkout_date=checkout.checkout_date)
    session.add(new_checkout)
    book = session.query(Book).filter(Book.id == new_checkout.book_id).first()

    if not book:
        raise Exception("Book not found.")
    
    if book.available_copies <= 0:
        raise Exception("No available copies.")

    book.available_copies -= 1
    session.commit()
    session.refresh(new_checkout)
    return new_checkout

# Handle someone making a return to the library
def return_checkout(checkout_id: int):
    target = session.query(Checkout).filter(Checkout.id == checkout_id).first()
    
    if target:
        book = session.query(Book).filter(Book.id == target.book_id).first()
        book.available_copies += 1
        session.delete(target)
        session.commit()

# Get checkout(s) by checkout ID
def get_checkout_id(checkout_id: int):
    target = session.query(Checkout).filter(Checkout.id == checkout_id).first()
    return target.to_dict()

# Get checkout(s) by user ID
def get_checkout_user_id(user_id: int):
    checkouts = session.query(Checkout).filter(Checkout.id == user_id).all()
    checkouts_dict = [checkout.to_dict() for checkout in checkouts]
    return checkouts_dict

# Get checkout(s) by book ID
def get_checkout_book_id(book_id: int):
    checkouts = session.query(Checkout).filter(Checkout.book_id == book_id).all()
    checkouts_dict = [checkout.to_dict() for checkout in checkouts]
    return checkouts_dict

# Get all checkouts
def get_checkouts():
    checkouts = session.query(Checkout).all()
    checkouts_dict = [checkout.to_dict() for checkout in checkouts]
    return checkouts_dict
