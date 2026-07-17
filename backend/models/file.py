from database.database import db
from datetime import datetime


class File(db.Model):

    __tablename__ = "files"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    filepath = db.Column(
        db.String(500),
        nullable=False
    )

    uploaded_by = db.Column(
        db.Integer,
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
