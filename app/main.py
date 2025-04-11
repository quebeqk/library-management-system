from fastapi import FastAPI
from .db import init_db
from contextlib import asynccontextmanager
from .routes.user_routes import router as user_router
from .routes.book_routes import router as book_router
from .routes.borrow_request_routes import router as borrow_request_router
from .routes.borrow_history_routes import router as borrow_history_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Register Routes
app.include_router(user_router)
app.include_router(book_router)
app.include_router(borrow_request_router)
app.include_router(borrow_history_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System!"}

