from sqlalchemy import Column, String, Integer, ForeignKey, or_
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    total_copies = Column(Integer)
    available_copies = Column(Integer)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author, "genre": self.genre, "total_copies": self.total_copies, "available_copies": self.available_copies}

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(String)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "role": self.role}


class Checkout(Base):
    __tablename__ = "checkouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    book_id = Column(Integer, ForeignKey(Book.id))
    checkout_date = Column(String)

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "book_id": self.book_id, "checkout_date": self.checkout_date}
