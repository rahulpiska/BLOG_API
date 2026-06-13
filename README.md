# Blog API

A RESTful Blog API built using FastAPI, SQLAlchemy, MySQL, Alembic, and JWT Authentication.

## Features

* User Registration
* User Login
* JWT Authentication
* Protected Routes
* Get Current User
* Posts CRUD
* Comments CRUD
* Like / Unlike Posts
* Authorization Checks
* Search Posts
* Pagination
* Sorting
* Alembic Database Migrations

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* MySQL
* Alembic
* Pydantic
* JWT
* Passlib
* Git & GitHub

## Project Structure

```text
BLOG_API/
├── routes/
│   ├── auth.py
│   ├── users.py
│   ├── posts.py
│   ├── comments.py
│   └── likes.py
├── alembic/
├── database.py
├── models.py
├── schemas.py
├── utils.py
├── main.py
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/rahulpiska/BLOG_API.git
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate virtual environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/blog_api_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run the application:

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Authentication

* POST /login
* GET /login/me

### Users

* POST /users

### Posts

* POST /posts
* GET /posts
* GET /posts/{id}
* GET /posts/{id}/details
* PUT /posts/{id}
* DELETE /posts/{id}

### Comments

* POST /comments/posts/{post_id}
* GET /comments
* PUT /comments/{comment_id}
* DELETE /comments/{comment_id}

### Likes

* POST /likes/posts/{post_id}

## Advanced Features

### Search

```http
GET /posts?search=fastapi
```

### Pagination

```http
GET /posts?skip=0&limit=10
```

### Sorting

```http
GET /posts?order=desc
GET /posts?order=asc
```

## Author

Rahul Piska
