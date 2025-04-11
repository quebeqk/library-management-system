# 📚 Library Management System API

A role-based Library Management System built using **FastAPI**, **MySQL**, and **JWT authentication**. This system allows users to request books and view their borrow history, while librarians can manage books and approve or deny borrow requests.

---

## 🚀 Features

### 👤 User & Librarian Roles

- User registration & login
- Role-based access:
  - `user`: Can request books, view own borrow requests & history
  - `librarian`: Can manage books and approve/deny borrow requests

### 📚 Book Management

- Add new books (librarian only)
- View all books

### 🔄 Borrow Requests

- Users can request to borrow books with a start and end date
- Librarians can **approve** or **deny** requests
- Soft deletion of borrow requests via status updates (e.g., `cancelled`)

### 🕓 Borrow History

- Automatically recorded when a borrow request is **approved**
- Includes status like: `borrowed`, `returned`, and `overdue`

### 🔐 Authentication & Authorization

- JWT-based login system
- Protected routes using `Depends`
- Role-based access with custom dependencies

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI
- **Database:** MySQL (via SQLAlchemy ORM)
- **Authentication:** JWT (JSON Web Tokens)
- **Dependencies:** `fastapi`, `pydantic`, `sqlalchemy`, `python-jose`, `passlib`, `bcrypt`

---
