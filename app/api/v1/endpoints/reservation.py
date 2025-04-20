from fastapi import APIRouter, Depends,HTTPException,status,BackgroundTasks
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
    background_task : BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Instantiate repositories inside the endpoint where db session is available
    product_repo = ProductRepository(db)
    reservation_repo = ReservationRepository(db)
    
    # Initialize the ReservationService with all required arguments
    reservation_service = ReservationService(db, product_repo, reservation_repo)
    
    try:
        # Create the reservation
        reservation_response = await reservation_service.reserve_product(reservation)
        background_task.add_task(reservation_service.release_expired_reservations)
        return reservation_response
    except ValueError as e:
        # Translate Python ValueError into an HTTP 400 Bad Request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
