from fastapi import FastAPI, Query, status
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from data_model import Base
from schemas import User, Book, Checkout, CheckoutCreate
from typing import Optional 
import database

# DB Location
DATABASE_URL = "sqlite:///./library.db"

# Create engine 
engine = create_engine(DATABASE_URL)

# Validate data model & bind classes to tables
Base.metadata.create_all(bind=engine)

# Create session factory
session_factory = sessionmaker(bind=engine)
session = session_factory()

app = FastAPI()

########### BEGIN BOOK ENDPOINTS ###########
# Get information for all books
@app.get("/books", status_code=status.HTTP_200_OK) 
def get_books(): 
    return database.get_books()

# Get information for books based on a title search query
@app.get("/books/{title}", status_code=status.HTTP_200_OK)
def get_books_by_title(title: str):
    return database.get_books_by_title(title)

# Get information about a specfic book by searching its ID
@app.get("/books/id/{book_id}", status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int):
    return database.get_book_by_id(book_id)

# Create a new book
@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    new_id = database.get_unique_book_id()
    book.id = new_id
    database.create_book(book) 
    return {"message": f"{book.total_copies} copies of {book.title} by {book.author} have been added to the system."}

# Update a book record
@app.patch("/books", status_code=status.HTTP_200_OK)
def update_book(book: Book):
    database.update_book(book)
    print(f"Book number {book.id} updated successfully.")

# Delete a book record
@app.delete("/books/{id}", status_code=status.HTTP_200_OK)
def delete_book(id: int):
    database.delete_book(id)
    print(f"Book {id} deleted.")

########### BEGIN USER ENDPOINTS ###########
# Create new user
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    new_id = database.get_unique_user_id()
    user.id = new_id
    database.create_user(user)
    return {"message": f"User {user.username} created successfully"}

# Get all user records
@app.get("/users", status_code=status.HTTP_200_OK)
def get_users():
    return database.get_users()

# Get user records by username search
@app.get("/users/username/{name}", status_code=status.HTTP_200_OK)
def get_users_by_username(name: str):
    return database.get_users_by_username(name)

# Get user record by searching  ID
@app.get("/users/id/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int):
    return database.get_user_by_id(user_id)

# Update user record
@app.patch("/users", status_code=status.HTTP_200_OK)
def update_user(user: User):
    database.update_user(user)
    print(f"User number {user.id} updated.")

@app.delete("/users/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int):
    database.delete_user(id)
    print(f"User number {id} deleted.")
    
########### BEGIN CHECKOUT ENDPOINTS ###########
# Create new record of a checkout
@app.post("/checkouts", status_code=status.HTTP_201_CREATED)
def create_checkout(checkout: CheckoutCreate):
    new_checkout = database.create_checkout(checkout)
    return {"message": f"Checkout number {new_checkout.id} created successfully."}

# Process a checked out item being returned
@app.delete("/checkouts/return/{checkout_id}", status_code=status.HTTP_200_OK) 
def return_checkout(checkout_id: int):
    database.return_checkout(checkout_id)
    return {"message": f"Checkout number {checkout_id} returned."}

# Get a record of a checkout by checkout ID
@app.get("/checkouts/{checkout_id}", status_code=status.HTTP_200_OK)
def get_checkout_by_checkout_id(checkout_id: int):
    database.get_checkout_id(checkout_id)

# Get checkouts that contain a specific user ID
@app.get("/checkouts/user/{user_id}")
def get_checkouts_by_user(user_id):
    return database.get_checkout_id(user_id)

# Get checkouts that contain a specific book ID
@app.get("/checkouts/book/{book_id}", status_code=status.HTTP_200_OK)
def get_checkouts_by_book(book_id: int):
    return database.get_checkout_book_id(book_id)

# Get all checkouts
@app.get("/checkouts", status_code=status.HTTP_200_OK)
def get_checkouts():
    return database.get_checkouts()
