from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import Numeric

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)

    username = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        index=True,
    )

    macho_bucks = db.Column(
        db.Numeric,
        default=0,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    bank_account_number = db.Column(
        db.BigInteger,
        default=999,
    )

    holdings = db.relationship(
        "Holding",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "macho_bucks": self.macho_bucks,
            "bank_account_number": self.bank_account_number,
        }

class Ranking(db.Model):
    __tablename__ = "rankings"

    id = db.Column(db.BigInteger, primary_key=True)

    username = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    bank_account_number = db.Column(
        db.BigInteger,
        default=999,
    )

    ranking = db.Column(
        db.String(64),
        default="norank",
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "bank_account_number": self.bank_account_number,
            "ranking": self.ranking,
        }

class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.BigInteger, primary_key=True)

    username = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )
