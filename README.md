# Student Management API

A RESTful API for managing student records, secured with JWT authentication
(access + refresh tokens). Built with FastAPI and SQLAlchemy.

## Features

- Full CRUD for student records (Create, Read, Update, Delete)
- User signup and login with securely hashed passwords (bcrypt)
- JWT-based authentication with access tokens and refresh tokens
- Refresh token rotation and logout/token revocation
- Public read endpoints, protected write endpoints
- Environment-based configuration (no secrets in source code)
- Automated tests with pytest
- Dockerized for easy deployment

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite (via SQLAlchemy ORM)
- **Auth:** JWT (python-jose), bcrypt password hashing (passlib)
- **Testing:** pytest, httpx
- **Deployment:** Docker

## Project Structure

```
student-management-api/
├── app/
│   ├── main.py           # App entrypoint, wires routers together
│   ├── config.py         # Environment-based settings
│   ├── database.py       # DB engine/session setup
│   ├── models.py         # SQLAlchemy table definitions
│   ├── schemas.py        # Pydantic request/response models
│   ├── auth.py           # Password hashing + JWT logic
│   └── routers/
│       ├── users.py      # Signup, login, refresh, logout
│       └── students.py   # Student CRUD routes
├── tests/
│   └── test_api.py
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Getting Started

### 1. Clone and set up environment

```bash
git clone <your-repo-url>
cd student-management-api
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Then open .env and set a real SECRET_KEY, e.g. generate one with:
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Run the app

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### 4. Run tests

```bash
pytest
```

### 5. Run with Docker (alternative to steps 1-3)

```bash
docker build -t student-api .
docker run -p 8000:8000 student-api
```

## API Endpoints

| Method | Endpoint             | Auth Required | Description                |
|--------|-----------------------|:--------------:|----------------------------|
| POST   | `/auth/signup`         | No             | Create a new user account  |
| POST   | `/auth/login`          | No             | Log in, receive tokens     |
| POST   | `/auth/refresh`        | No*            | Exchange refresh token for new access token |
| POST   | `/auth/logout`         | Yes            | Revoke refresh token       |
| GET    | `/students/`           | No             | List all students          |
| GET    | `/students/{id}`       | No             | Get one student by ID      |
| GET    | `/students/by-name/{name}` | No        | Get one student by name    |
| POST   | `/students/`           | Yes            | Create a student            |
| PUT    | `/students/{id}`       | Yes            | Update a student           |
| DELETE | `/students/{id}`       | Yes            | Delete a student           |

\* requires a valid refresh token in the request body instead of a header

## Authentication Flow

1. `POST /auth/signup` — create an account (password is hashed with bcrypt before storage)
2. `POST /auth/login` — receive an `access_token` (30 min expiry) and `refresh_token` (7 day expiry)
3. Include the access token on protected routes: `Authorization: Bearer <access_token>`
4. When the access token expires, call `POST /auth/refresh` with the refresh token to get a new pair
5. `POST /auth/logout` revokes the stored refresh token

## Future Improvements

- Role-based access control (admin vs regular user)
- Rate limiting on login/signup routes
- PostgreSQL for production instead of SQLite
- CI pipeline (GitHub Actions) running tests on every push
