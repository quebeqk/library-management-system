from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from ..utils.utils import hash_password
from ..utils.auth import create_access_token
from ..utils.utils import verify_password
from ..dependencies import get_current_user, require_librarian

router = APIRouter(prefix="/user", tags=["Users"])

# Get Current User (requires authentication)
@router.get("/me", response_model = UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# OAuth2 /token route for Swagger UI
@router.post("/token", response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(form_data.password, str(user.password)):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# User Login Route
@router.post("/login", response_model= TokenResponse) 
def login(user: UserLogin,db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail= "Invalid email or password")
    
    if not verify_password(user.password, str(db_user.password)):
        raise HTTPException(status_code=401, detail= "Invalid email or password")
    
    access_token = create_access_token({"user_id": db_user.id, "role": db_user.role})

    return {"access_token" : access_token, "token_type": "bearer"}


# Create User
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password before storing it
    hashed_password = hash_password(user.password)

    # Create new user
    new_user = User(
        name = user.name,
        email = user.email,
        password = hashed_password,
        role = user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get All Users
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    return db.query(User).all()

# Get User by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete User
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_librarian)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}