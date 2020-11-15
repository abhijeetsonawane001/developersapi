from app.models import Developer
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2)])
    email_id = StringField("Email ID", validators=[DataRequired(), Email()])
    submit = SubmitField("Get Started")

    def validate_email_id(self, email_id):
        developer = Developer.query.filter_by(email_id=email_id.data).first()
        if developer:
            raise ValidationError(
                "Email ID already exists! Please try with another one."
            )


class LoginForm(FlaskForm):
    email_id = StringField("Email ID", validators=[DataRequired(), Email()])
    submit = SubmitField("Login")

    def validate_email_id(self, email_id):
        developer = Developer.query.filter_by(email_id=email_id.data).first()
        if not developer:
            raise ValidationError("Email ID not exist!")


class OTPVerifyForm(FlaskForm):
    otp = StringField("OTP", validators=[DataRequired()])
    submit = SubmitField("Verify OTP")


class CreateApiToken(FlaskForm):
    api_name = StringField("API Token Name", validators=[DataRequired()])
    api_valid_till = IntegerField("API Token Valid Till (In minutes)")
    submit = SubmitField("Generate")
