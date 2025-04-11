from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Book, User
from ..schemas import BookCreate, BookResponse
from ..dependencies import require_librarian

router = APIRouter(prefix="/books", tags=["Books"])

# Create a Book
@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Get All Books
@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

# Get Book by ID
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update Book (e.g., Update available copies)
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookCreate, db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_update.model_dump().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book

# Delete Book
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
