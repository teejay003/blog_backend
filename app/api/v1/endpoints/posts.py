from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import post as schemas
from app.services import post as services
from app.services.user import get_current_user
from typing import List, Optional, Dict

    
router = APIRouter()

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return services.create_post(db, post, current_user)

@router.put("/{post_id}")
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return services.update_post(db, post_id, post, current_user)

@router.get("", response_model=schemas.PostResponse) 
def list_posts(
    db: Session = Depends(get_db),
    limit: int = Query(10, description="Number of posts per page"),
    offset: int = Query(0, description="Offset for pagination"),
    ):
    """Retrieve all blog posts."""
    return services.list_all_posts(db, limit=limit, offset=offset)

@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Retrieve a blog post by ID."""
    return services.get_post_by_id(db, post_id)

@router.get("/filter/", response_model=List[schemas.Post])
def filter_posts(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None, description="Filter by post title"),
    author_id: Optional[int] = Query(None, description="Filter by author ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Filter posts by title, author, or date range."""
    return services.get_filtered_posts(db, title, author_id, start_date, end_date)
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return services.delete_post(db, post_id, current_user)

@router.post("/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return services.like_post(db, post_id, current_user)

@router.post("/{post_id}/comment")
def add_comment(
    post_id: int, 
    request: schemas.Comment, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    return services.add_comment(db, post_id, request.comment_text, current_user)
