import secrets
import string
from datetime import datetime, timedelta

from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Developer.query.get(user_id)


class Developer(db.Model, UserMixin):

    __tablename__ = "developers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email_id = db.Column(db.String(255), nullable=False)
    login_otp = db.Column(db.String(255), nullable=True, unique=True)
    login_otp_created_at = db.Column(db.DateTime, nullable=True)
    login_otp_valid_till = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    api_tokens = db.relationship("ApiToken", backref="developer", lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __repr__(self):
        return "Developer: {}".format(self.id)

    def create_login_otp(self, valid_second=3600):
        digits = string.digits
        otp = "".join(secrets.choice(digits) for i in range(6))
        self.login_otp = otp
        self.login_otp_created_at = datetime.utcnow()
        self.login_otp_valid_till = valid_second

        return self.login_otp

    def verify_login_otp(self, login_otp):
        if not self.login_otp:
            return False

        current_timestamp = datetime.now()
        valid_till = current_timestamp + timedelta(seconds=self.login_otp_valid_till)

        return self.login_otp == login_otp and current_timestamp < valid_till

    def delete_login_otp(self):
        self.login_otp = None
        self.login_otp_created_at = None
        self.login_otp_valid_till = None
