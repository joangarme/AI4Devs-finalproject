"""
User model for authentication and user management.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """
    User model representing a registered user in the system.
    
    Attributes:
        id: Unique identifier for the user
        email: User's email address (unique)
        password_hash: Bcrypt hashed password
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
        is_active: Whether the user account is active (MVP: always True on registration)
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', is_active={self.is_active})>"

    def to_dict(self, exclude_password: bool = True) -> dict:
        """
        Convert the user model to a dictionary.
        
        Args:
            exclude_password: If True, excludes password_hash from the result
            
        Returns:
            Dictionary representation of the user
        """
        data = {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }
        
        if not exclude_password:
            data["password_hash"] = self.password_hash
            
        return data

