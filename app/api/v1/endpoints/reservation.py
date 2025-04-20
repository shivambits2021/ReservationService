from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.domain.services.reservation_service import ReservationService
from app.repositories.product_repository import ProductRepository
from app.repositories.reservation_repository import ReservationRepository
from app.schemas.reservation import ReservationCreate, ReservationResponse

router = APIRouter()

@router.post("/reserve", response_model=ReservationResponse)
async def reserve_product(
    reservation: ReservationCreate,
    db: Session = Depends(get_db)
):
    # Instantiate repositories inside the endpoint where db session is available
    product_repo = ProductRepository(db)
    reservation_repo = ReservationRepository(db)
    
    # Initialize the ReservationService with all required arguments
    reservation_service = ReservationService(db, product_repo, reservation_repo)
    
    try:
        return await reservation_service.reserve_product(reservation)
    except ValueError as e:
        # Translate Python ValueError into an HTTP 400 Bad Request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
