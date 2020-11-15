import hashlib
import secrets
from datetime import datetime

from app import db


class ApiToken(db.Model):
    __tablename__ = "api_tokens"

    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(255), nullable=False)
    api_token = db.Column(db.Text(), unique=True, nullable=True)
    api_token_valid_till = db.Column(db.Integer, nullable=True)
    developer_id = db.Column(db.Integer, db.ForeignKey("developers.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __repr__(self):
        return "ApiToken: {}".format(self.id)

    def generate_api_token(self):
        token = secrets.token_urlsafe(40)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        self.api_token = token_hash

        return token
