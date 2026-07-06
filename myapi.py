from fastapi import FastAPI, HTTPException, Path, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Student as StudentModel
import models

# This line creates the actual table in students.db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ==========================================
# Pydantic schemas (for request/response)
# ==========================================

class StudentCreate(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


# ==========================================
# ROUTES
# ==========================================

# GET all students
@app.get("/")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(StudentModel).all()
    return students


# GET one student by ID
@app.get("/get-student/{student_id}")
def get_student(
    student_id: int = Path(description="The ID of the student", gt=0),
    db: Session = Depends(get_db)
):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


# GET student by name
@app.get("/get-by-name")
def get_by_name(name: str, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(
        StudentModel.name == name
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


# POST - create new student
@app.post("/create-student")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if student with same name already exists
    existing = db.query(StudentModel).filter(
        StudentModel.name == student.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Student already exists"
        )
    
    # Create new student object
    new_student = StudentModel(
        name=student.name,
        age=student.age,
        year=student.year
    )
    
    # Save to database
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student


# PUT - update existing student
@app.put("/update-student/{student_id}")
def update_student(
    student_id: int,
    student: UpdateStudent,
    db: Session = Depends(get_db)
):
    # Find student in database
    db_student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()
    
    if not db_student:
        raise HTTPException(
            status_code=404, 
            detail="Student not found"
        )
    
    # Only update fields that were provided
    if student.name is not None:
        db_student.name = student.name
    if student.age is not None:
        db_student.age = student.age
    if student.year is not None:
        db_student.year = student.year
    
    # Save changes
    db.commit()
    db.refresh(db_student)
    
    return db_student


# DELETE - delete a student
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=404, 
            detail="Student not found"
        )
    
    db.delete(student)
    db.commit()
    
    return {"Message": "Student deleted successfully"}