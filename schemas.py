from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    total_copies: int
    available_copies: int

class BookCreate(BookBase):
    title: str
    author: str
    genre: str
    total_copies: int
    available_copies: int

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    username: str
    role: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    role: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class CheckoutBase(BaseModel):
    user_id: int
    book_id: int
    checkout_date: str

class CheckoutCreate(CheckoutBase):
    user_id: int
    book_id: int
    checkout_date: str

class CheckoutUpdate(CheckoutBase):
    user_id: Optional[int] = None
    book_id: Optional[int] = None
    checkout_date: Optional[str] = None

class Checkout(CheckoutBase):
    id: int

    class Config:
        from_attributes = True
