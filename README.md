# FastAPI Blog API

This is a backend API built with **FastAPI** for a blog application. It supports user authentication, admin management, post creation, comments, and likes.

## Features
- ✅ User Registration (Normal Users & Admins)
- ✅ User Authentication (JWT-based)
- ✅ CRUD Operations for Blog Posts
- ✅ Admin-only Post Management
- ✅ Likes & Comments on Posts

## Installation

### 1️⃣ Clone the repository
```bash
git clone git@github.com:ifeoluwashola/blog_backend.git
cd blog_backend
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create Database Migration file
Modify `database.py` to configure your database connection.

Run database migrations:
```bash
alembic upgrade head
```

### 5️⃣ Start the server
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
| Method | Endpoint               | Description |
|--------|------------------------|-------------|
| POST   | `/api/v1/users/register` | Register a new user |
| POST   | `/api/v1/users/login`    | Login and receive JWT token |
| POST   | `/api/v1/users/create-admin` | Create an admin (admin-only) |

### Blog Posts
| Method | Endpoint        | Description |
|--------|----------------|-------------|
| GET    | `/api/v1/posts` | Get all posts |
| POST   | `/api/v1/posts` | Create a new post (admin-only) |
| PUT    | `/api/v1/posts/{id}` | Edit a post (admin-only) |
| DELETE | `/api/v1/posts/{id}` | Delete a post (admin-only) |

### Likes & Comments
| Method | Endpoint                 | Description |
|--------|--------------------------|-------------|
| POST   | `/api/v1/posts/{id}/like` | Like a post |
| POST   | `/api/v1/posts/{id}/comment` | Add a comment to a post |

## Environment Variables
Create a `.env` file and add:
```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Dependencies

Here is the `requirements.txt` file with all the necessary dependencies:

```
fastapi
uvicorn
pydantic
sqlalchemy
alembic
passlib[bcrypt]
python-jose[cryptography]
python-multipart
databases
```

## License
This project is licensed under the MIT License.

