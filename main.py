from fastapi import FastAPI, Query, status
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from data_model import Base
from schemas import User, Book, Checkout
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
# Get information for books
@app.get("/books", status_code=status.HTTP_200_OK) # CHANGE STATUS CODE FOR GET REQUEST IF NEEDED
def get_books(name: Optional[str] = None):
    print(database.get_books(name)) # OUTPUT FOR TESTING
    return database.get_books(name)

# Create a new book
@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    database.create_book(book) 
    return {"message": f"{book.total_copies} copies of {book.title} by {book.author} have been added to the system."} # MAY NOT NEED THIS (OR MAY HANDLE DIFFERENTLY)

# Update a book
@app.patch("/books", status_code=status.HTTP_200_OK)
def update_book(book: Book):
    database.update_book(book)
    print(f"Book number {book.id} updated successfully.") # HAVE A TESTING OUTPUT TO THE TERMINAL

@app.delete("/books", status_code=status.HTTP_200_OK)
def delete_book(id: int):
    database.delete_book(id)
    print(f"Book {id} deleted.")

########### BEGIN USER ENDPOINTS ###########
# Create new user
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    User.create_user(user) # WAS ORIGINALLY: User.create_user(session, user)
    return {"message": "User created successfully"}

@app.get("/users") # CHANGE STATUS CODE FOR GET REQUEST IF NEEDED - originally included: status_code=status.HTTP_200_OK
def get_user(name: Optional[str] = None):
    print(database.get_user(name)) # OUTPUT FOR TESTING
    return database.get_user(name)

@app.patch("/users")
def update_user(user: User):
    database.update_user(user)
    print(f"User {user.id} updated.")

@app.delete("/users")
def delete_user(id: int):
    database.delete_user(id)
    print(f"Book {id} deleted.")
    
########### BEGIN CHECKOUT ENDPOINTS ###########
@app.post("/checkout", status_code=status.HTTP_201_CREATED)  #   *FINISH THIS ONE*
def create_checkout(checkout: Checkout):
    database.create_checkout(checkout)
    return {"message": f"Checkout number {checkout.id} created successfully."}

@app.post("/return") # SHOULD CHANGE TO PATCH?
def return_checkout(checkout_id: int):
    database.return_checkout(checkout_id)
    return {"message": f"Checkout number {checkout_id} returned."}

@app.get("/checkouts/user/{user_id}")
def get_checkout_user(user_id):
    return database.get_checkout_id(user_id) # CONFIRM THIS IS WORKING

@app.get("/checkouts/all")
def get_checkouts():
    return database.get_checkouts()