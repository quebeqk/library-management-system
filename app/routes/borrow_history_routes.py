from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import BorrowHistory, User
from ..schemas import BorrowHistoryResponse
from ..dependencies import require_librarian, get_current_user, require_user


router = APIRouter(prefix="/borrow-history", tags=["Borrow History"])

#Get all borrow history record for user
@router.get("/me", response_model=list[BorrowHistoryResponse])
def get_my_history(db: Session = Depends(get_db), current_user: User = Depends(require_user)):
    return db.query(BorrowHistory).filter(
        BorrowHistory.user_id == current_user.id,
        BorrowHistory.status.in_(["borrowed", "returned", "overdue"])
    ).all()

# Get All Borrow History Records
@router.get("/", response_model=list[BorrowHistoryResponse])
def get_all_borrow_history(db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    return db.query(BorrowHistory).filter(
        BorrowHistory.status.in_(["borrowed", "returned", "overdue"])
    ).all()


# Get Borrow History by User ID
@router.get("/user/{user_id}", response_model=list[BorrowHistoryResponse])
def get_borrow_history_by_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_librarian)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db.query(BorrowHistory).filter(
        BorrowHistory.user_id == user_id,
        BorrowHistory.status.in_(["borrowed", "returned", "overdue"])
    ).all()

