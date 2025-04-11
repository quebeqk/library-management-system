from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

# Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    name = Column(String(255), nullable=False) 
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("user", "librarian", name="user_roles"), default="user", nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    borrow_requests = relationship("BorrowRequest", back_populates="user")
    borrow_history = relationship("BorrowHistory", back_populates="user")

# Book Table
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(255), unique= True, nullable=True)
    available_copies = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now()) 

    borrow_requests = relationship("BorrowRequest", back_populates="book")
    borrow_history = relationship("BorrowHistory", back_populates="book")

# Borrow Requests Table
class BorrowRequest(Base):
    __tablename__ = "borrow_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(Enum("pending", "approved", "denied", name="request_status"), default="pending")

    user = relationship("User", back_populates="borrow_requests")
    book = relationship("Book", back_populates="borrow_requests")

# Borrow History Table
class BorrowHistory(Base):
    __tablename__ = "borrow_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(Enum("borrowed", "returned", "overdue", name="history_status"), default="borrowed", nullable=False)

    user = relationship("User", back_populates="borrow_history")
    book = relationship("Book", back_populates="borrow_history")

    