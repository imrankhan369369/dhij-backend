from fastapi import FastAPI

from app.database import engine
from app import models
from app.routers import  users, providers,bookings

# This line creates the actual tables (students, users) in students.db,
# based on the model classes in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DHIJ API",
    description="A CRUD API for managing users, with JWT authentication",
    version="1.0.0",
)

# Plugging in our two routers.
# Every route defined in users.py now lives under /auth/...
# Every route defined in students.py now lives under /students/...
app.include_router(users.router)
app.include_router(providers.router)
app.include_router(bookings.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "API is running"}
