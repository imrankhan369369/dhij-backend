from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a file called students.db in your folder
DATABASE_URL = "sqlite:///./students.db"

# Create engine - this is your connection to the database
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Every database table will inherit from this
Base = declarative_base()

# This creates a session - think of it like opening 
# a conversation with your database
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# This function gives us a database session
# We will use this in every route
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()