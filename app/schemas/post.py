from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CommentBase(BaseModel):
    comment_text: Optional[str]

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass
    
class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    likes: List[int]  # ✅ Ensure `likes` is a list of user IDs
    comments: List[Comment] = []

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_likes(cls, post):
        """Convert Post ORM model to Pydantic schema, extracting user IDs for likes"""
        return cls(
            id=post.id,
            title=post.title,
            content=post.content,
            author_id=post.author_id,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes=[user.id for user in post.likes],  # ✅ Ensure likes are user IDs
            comments=[
                Comment.model_validate(comment) if comment else None  
                for comment in post.comments or []  # ✅ Handle missing comments properly
            ],
        )

class PostResponse(BaseModel):
    total: int
    posts: List[Post]