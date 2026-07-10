from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student as StudentModel, User as UserModel
from app.schemas import StudentCreate, UpdateStudent, StudentResponse
from app.routers.users import get_current_user

router = APIRouter(prefix="/students", tags=["Students"])


# GET all students — open to anyone (no login required)
@router.get("/", response_model=list[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()


# GET one student by ID
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int = Path(description="The ID of the student", gt=0),
    db: Session = Depends(get_db),
):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# GET student by name
@router.get("/by-name/{name}", response_model=StudentResponse)
def get_by_name(name: str, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.name == name).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# POST - create new student — now PROTECTED: must be logged in
@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    existing = db.query(StudentModel).filter(StudentModel.name == student.name).first()

    if existing:
        raise HTTPException(status_code=400, detail="Student already exists")

    new_student = StudentModel(
        name=student.name,
        age=student.age,
        year=student.year,
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# PUT - update existing student — PROTECTED
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: UpdateStudent,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.name is not None:
        db_student.name = student.name
    if student.age is not None:
        db_student.age = student.age
    if student.year is not None:
        db_student.year = student.year

    db.commit()
    db.refresh(db_student)

    return db_student


# DELETE - delete a student — PROTECTED
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
