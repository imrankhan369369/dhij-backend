from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Provider as ProviderModel, User as UserModel
from app.schemas import ProviderCreate, ProviderResponse
from app.routers.users import get_current_user, get_current_admin

router = APIRouter(prefix="/providers", tags=["Providers"])


# GET all providers — public, so visitors can browse before signing up
@router.get("/", response_model=list[ProviderResponse])
def get_all_providers(db: Session = Depends(get_db)):
    return db.query(ProviderModel).all()


# GET one provider by ID — public
@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(ProviderModel).filter(
        ProviderModel.id == provider_id
    ).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider


# POST create a provider — protected, only logged-in users can add
@router.post("/", response_model=ProviderResponse, status_code=201)
def create_provider(
    provider: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin),
):
    new_provider = ProviderModel(
        name=provider.name,
        offering=provider.offering,
        bio=provider.bio,
    )

    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)

    return new_provider