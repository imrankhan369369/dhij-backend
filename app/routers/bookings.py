import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking as BookingModel, Provider as ProviderModel, User as UserModel
from app.schemas import BookingCreate, BookingResponse
from app.routers.users import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# POST create a booking — protected, tied to whoever is logged in
@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Make sure the provider being booked actually exists
    provider = db.query(ProviderModel).filter(
        ProviderModel.id == booking.provider_id
    ).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    # Generate a unique Jitsi meeting link - no video code needed,
    # just a unique URL that Jitsi will turn into a live room when visited
    room_name = f"DHIJ-{uuid.uuid4().hex[:10]}"
    meeting_link = f"https://meet.jit.si/{room_name}"

    new_booking = BookingModel(
        user_id=current_user.id,
        provider_id=booking.provider_id,
        scheduled_time=booking.scheduled_time,
        meeting_link=meeting_link,
        status="confirmed",
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


# GET all bookings for the currently logged-in user
@router.get("/my-bookings", response_model=list[BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return db.query(BookingModel).filter(
        BookingModel.user_id == current_user.id
    ).all()


# GET one booking by id — only the user who owns it can view it
@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    booking = db.query(BookingModel).filter(
        BookingModel.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")

    return booking