import os
from typing import List, Optional
from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, \
    mapped_column, relationship, validates
from uuid import UUID
from datetime import datetime
from utils import DB_FOLDER, UPLOADS_FOLDER, \
    OUTPUTS_FOLDER, UploadStatus
from email_validate import validate

DB_PATH = os.path.join(DB_FOLDER, "db.sqlite3")

class Base(DeclarativeBase):
    pass

class User(Base):
    """
    User entity - represents a user in the system.
    Holds the user's email and a list of uploads.
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    uploads: Mapped[List["Upload"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @validates("email")
    def validate_email(self, key, email):
        if not validate(email):
            raise ValueError("Invalid email address.")
        return email


class Upload(Base):
    """
    Upload entity - represents an upload in the system.
    Holds the upload UID, filename, upload time, finish time, status
    and the user who uploaded it.
    """
    __tablename__ = "uploads"
    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[UUID] = mapped_column(nullable=False, unique=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    upload_time: Mapped[datetime] = mapped_column(nullable=False)
    finish_time: Mapped[datetime] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False,
                                        default=UploadStatus.PENDING)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="uploads")

    @property
    def upload_name(self) -> str:
        """
        Get the name of the uploaded file.
        """
        return str(self.uid)

    @property
    def upload_path(self) -> str:
        """
        Get the path of the uploaded file.
        """
        return os.path.join(UPLOADS_FOLDER, self.upload_name)

    @property
    def output_name(self) -> str:
        """
        Get the name of the output file.
        """
        return str(self.uid) + '.json'

    @property
    def output_path(self) -> str:
        """
        Get the path of the output file.
        """
        return os.path.join(OUTPUTS_FOLDER, self.output_name)


# create the database engine and create the tables
engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(engine)
