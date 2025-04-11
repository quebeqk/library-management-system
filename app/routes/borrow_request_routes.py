from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import BorrowRequest, User, Book, BorrowHistory
from ..schemas import BorrowRequestCreate, BorrowRequestResponse
from ..dependencies import require_user, require_librarian

router = APIRouter(prefix="/borrow-requests", tags=["Borrow Requests"])

# Create a Borrow Request
@router.post("/", response_model=BorrowRequestResponse)
def create_borrow_request(request: BorrowRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(require_user)):

    # Check if book exists
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Create a new borrow request with logged-in user ID
    borrow_request = BorrowRequest(
        user_id=current_user.id,
        book_id=request.book_id,
        start_date=request.start_date,
        end_date=request.end_date
    )
    db.add(borrow_request)
    db.commit()
    db.refresh(borrow_request)
    return borrow_request

# Get All Borrow Requests librarian
@router.get("/", response_model=list[BorrowRequestResponse])
def get_borrow_requests(db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    return db.query(BorrowRequest).all()

# Get All Borrow Requests User only 
@router.get("/me", response_model=list[BorrowRequestResponse])
def get_my_borrow_requests(db: Session = Depends(get_db), current_user: User = Depends(require_user)):
    return db.query(BorrowRequest).filter(BorrowRequest.user_id == current_user.id).all()

# Get Borrow Request by ID
@router.get("/{request_id}", response_model=BorrowRequestResponse)
def get_borrow_request(request_id: int, db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    borrow_request = db.query(BorrowRequest).filter(BorrowRequest.id == request_id).first()
    if not borrow_request:
        raise HTTPException(status_code=404, detail="Borrow request not found")
    return borrow_request

# Update Borrow Request Status (Approve/Deny)
@router.put("/{request_id}", response_model=BorrowRequestResponse)
def update_borrow_request(request_id: int, status: str, db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    borrow_request = db.query(BorrowRequest).filter(BorrowRequest.id == request_id).first()
    if not borrow_request:
        raise HTTPException(status_code=404, detail="Borrow request not found")

    if status not in ["pending", "approved", "denied"]:
        raise HTTPException(status_code=400, detail="Invalid status value")

    borrow_request.status = status
    db.commit()
    db.refresh(borrow_request)

    # Insert into borrowHistory if approved
    if status == "approved":
        # Check if already added in history (prevent duplicates if route called twice)
        existing_history = db.query(BorrowHistory).filter(
            BorrowHistory.user_id == borrow_request.user_id,
            BorrowHistory.book_id == borrow_request.book_id,
            BorrowHistory.start_date == borrow_request.start_date
        ).first()

        if not existing_history:
            history_entry = BorrowHistory(
                user_id=borrow_request.user_id,
                book_id=borrow_request.book_id,
                start_date=borrow_request.start_date,
                end_date=borrow_request.end_date,
                status="borrowed"
            )
            db.add(history_entry)
            db.commit()

    return borrow_request

# Delete Borrow Request
@router.delete("/{request_id}")
def delete_borrow_request(request_id: int, db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    borrow_request = db.query(BorrowRequest).filter(BorrowRequest.id == request_id).first()
    if not borrow_request:
        raise HTTPException(status_code=404, detail="Borrow request not found")

    db.delete(borrow_request)
    db.commit()
    return {"message": "Borrow request deleted successfully"}
