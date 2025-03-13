from sqlalchemy.orm import Session
from app.models import user as models
from app.schemas import user as schemas
from app.core import security
from app.db.session import get_db
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

auth_scheme = HTTPBearer()  

def create_admin_user(db: Session, user: schemas.UserCreate):
    """Create an admin user (only an existing admin can do this)."""
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = security.get_password_hash(user.password)
    admin_user = models.User(username=user.username, hashed_password=hashed_password, is_admin=True, is_superuser=True)
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    return admin_user

def get_user_by_username(db: Session, username: str):
    """Fetch user by username."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user."""
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user with username and password."""
    user = get_user_by_username(db, username)
    if not user or not security.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

def login_for_access_token(username: str, password: str, db: Session):
    """Login user and return access and refresh tokens."""
    user = authenticate_user(db, username, password)
    access_token = security.create_access_token(data={"sub": user.username})
    refresh_token = security.create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "is_admin": user.is_admin}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)):
    """Get the current logged-in user from the token."""
    token = credentials.credentials
    payload = security.verify_token(token)
    username: str = payload.get("sub")
    
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user
