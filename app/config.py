import os
import secrets

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    )
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = os.environ.get("MAIL_PORT", "25")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "admin@openspot.in")


class ProductionConfig(BaseConfig):
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", True)


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///{}".format(os.path.join(CONFIG_DIR, "database.db"))
    )
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = os.environ.get("MAIL_PORT", "25")


class TestConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///{}".format(os.path.join(CONFIG_DIR, "database.db"))
    )
