from sqlalchemy.orm import Session
from app.models import post as models
from app.schemas import post as schemas
from fastapi import HTTPException, status
from typing import List, Optional

def create_post(db: Session, post: schemas.PostCreate, current_user):
    """Only admin can create posts."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create posts")

    if not current_user.id:  # Ensure author_id is assigned
        raise HTTPException(status_code=400, detail="Invalid user")

    db_post = models.Post(title=post.title, content=post.content, author_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: schemas.PostCreate, current_user):
    """Only admin can update posts."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to edit posts")

    for key, value in post_update.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post

def list_all_posts(db: Session):
    """Retrieve all posts."""
    return db.query(models.Post).all()

def get_post_by_id(db: Session, post_id: int):
    """Retrieve a post by its ID."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

def get_filtered_posts(
    db: Session,
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[models.Post]:
    """Retrieve posts based on optional filters."""
    query = db.query(models.Post)

    if title:
        query = query.filter(models.Post.title.ilike(f"%{title}%"))
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    if start_date and end_date:
        query = query.filter(models.Post.created_at.between(start_date, end_date))

    return query.all()

def delete_post(db: Session, post_id: int, current_user):
    """Only admin can delete posts."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete posts")

    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}

def like_post(db: Session, post_id: int, current_user):
    """Users can like/unlike a post."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user in db_post.likes:
        db_post.likes.remove(current_user)  # Unlike
    else:
        db_post.likes.append(current_user)  # Like
    
    db.commit()
    return {"message": "Post liked/unliked successfully"}

def add_comment(db: Session, post_id: int, comment_text: str, current_user):
    """Users can add comments to posts."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = models.Comment(content=comment_text, post_id=post_id, user_id=current_user.id)
    db.add(comment)
    db.commit()
    return {"message": "Comment added successfully"}
