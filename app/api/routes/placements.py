from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.placement import Placement
from app.schemas.placement import PlacementCreate, PlacementOut, PlacementUpdate
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/placements", tags=["placements"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PlacementOut)
def create_placement(
    placement: PlacementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_placement = Placement(**placement.dict())
    db.add(new_placement)
    db.commit()
    db.refresh(new_placement)
    return new_placement


@router.patch("/{placement_id}", response_model=PlacementOut)
def update_placement(
    placement_id: int,
    placement_update: PlacementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    placement = db.query(Placement).filter(Placement.id == placement_id).first()
    if not placement:
        raise HTTPException(status_code=404, detail="Placement not found")

    update_data = placement_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(placement, field, value)

    db.commit()
    db.refresh(placement)
    return placement
