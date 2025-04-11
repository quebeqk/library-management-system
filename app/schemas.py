from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date

# User Schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["librarian", "user"]  

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

# Book Schema
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str]
    available_copies: Optional[int] = 1

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: Optional[str]
    available_copies: int

    class Config:
        from_attributes = True

# Borrow Request Schema
class BorrowRequestCreate(BaseModel):
    book_id: int
    start_date: date
    end_date: date

class BorrowRequestResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    start_date: date
    end_date: date
    status: str

    class Config:
        from_attributes = True

# Borrow History Schema

class BorrowHistoryResponse(BaseModel):
    id: int
    user_id: int  
    book_id: int  
    start_date: date
    end_date: Optional[date] = None
    status: str

    class Config:
        from_attributes = True



# Schema for user login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for login response (returns access token)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"