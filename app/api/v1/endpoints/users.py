from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import user as schemas
from app.services import user as services

router = APIRouter()

@router.post("/register/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return services.create_user(db, user)

@router.post("/create-admin/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_admin_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user),
):
    """Only an admin can create another admin."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create admin users")
    
    return services.create_admin_user(db, user)

@router.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Authenticate user and return access & refresh tokens."""
    return services.login_for_access_token(user.username, user.password, db)

@router.get("/me/", response_model=schemas.User)
def get_current_user_info(current_user: schemas.User = Depends(services.get_current_user)):
    """Get the logged-in user's info."""
    return current_user
