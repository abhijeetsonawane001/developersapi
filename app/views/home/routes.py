from datetime import timedelta

from app import db
from app.models import ApiToken, Developer
from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from .forms import CreateApiToken, LoginForm, OTPVerifyForm, RegisterForm
from .utils import send_login_mail

home = Blueprint("home", __name__)


@home.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for(".dashboard"))
    return render_template("home/index.html")


@home.route("/auth/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        developer = Developer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email_id=form.email_id.data,
        )
        db.session.add(developer)
        login_otp = developer.create_login_otp()
        db.session.commit()

        try:
            send_login_mail(form.email_id.data, login_otp)
        except Exception as e:
            current_app.logger.error("Unable to Email.")
            current_app.logger.error(e)

        session["developer_email"] = developer.email_id

        return redirect(url_for(".otp_verify"))

    return render_template("home/register.html", form=form)


@home.route("/auth/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        developer = Developer.query.filter_by(email_id=form.email_id.data).first()
        if developer:
            login_otp = developer.create_login_otp()
            db.session.commit()
            try:
                send_login_mail(form.email_id.data, login_otp)
            except Exception as e:
                current_app.logger.error("Unable to Email.")
                current_app.logger.error(e)
            session["developer_email"] = form.email_id.data
            return redirect(url_for(".otp_verify", next=request.args.get("next")))
    return render_template("home/login.html", form=form)


@home.route("/auth/verify", methods=["GET", "POST"])
def otp_verify():
    if "developer_email" not in session:
        return redirect(url_for(".login"))
    form = OTPVerifyForm()

    if form.validate_on_submit():
        developer = Developer.query.filter_by(
            email_id=session["developer_email"], login_otp=form.otp.data
        ).first()

        if developer:
            if developer.verify_login_otp(form.otp.data):
                if developer.is_active is False:
                    developer.is_active = True
                login_user(developer)
                session.pop("developer_email")
                developer.delete_login_otp()
                db.session.commit()
                if request.args.get("next"):
                    return redirect(request.args.get("next"))
                else:
                    return redirect(url_for(".dashboard"))
            else:
                flash(u"OTP Expired.", "danger")
                return redirect(url_for(".otp_verify"))
        else:
            flash(u"Invalid OTP.", "danger")
            return redirect(url_for(".otp_verify"))
    return render_template("home/otp_verify.html", form=form)


# Authenticated Developer Routes
@home.route("/dashboard")
@login_required
def dashboard():
    return render_template("home/dashboard.html", title="Dashboard")


@home.route("/setting")
@login_required
def setting():
    return render_template("home/setting.html", title="Setting")


@home.route("/auth/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".index"))


@home.route("/setting/api-tokens")
@login_required
def list_api_token():
    api_tokens = ApiToken.query.filter_by(developer_id=current_user.id).all()
    for api_token in api_tokens:
        api_token.api_token_valid_till = api_token.created_at + timedelta(
            minutes=api_token.api_token_valid_till
        )
    return render_template(
        "home/list_api_token.html", title="API Tokens", api_tokens=api_tokens
    )


@home.route("/setting/api-token/create", methods=["GET", "POST"])
@login_required
def create_api_token():
    form = CreateApiToken()
    if form.validate_on_submit():
        api_token = ApiToken(
            api_name=form.api_name.data,
            api_token_valid_till=form.api_valid_till.data,
            developer_id=current_user.id,
        )
        token = api_token.generate_api_token()
        db.session.add(api_token)
        db.session.commit()
        return render_template(
            "home/create_api_token.html",
            title="{} - API Token".format(api_token.api_name),
            api_token=api_token,
            token=token,
        )
    return render_template(
        "home/create_api_token.html", title="Create API Token", form=form
    )


@home.route(
    "/setting/api-token/delete/<int:token_id>/<int:developer_id>"
)
@login_required
def delete_api_token(token_id, developer_id):
    api_token = ApiToken.query.filter_by(id=token_id, developer_id=developer_id).first()
    if not api_token:
        abort(404)

    db.session.delete(api_token)
    db.session.commit()
    return redirect(url_for(".list_api_token"))
