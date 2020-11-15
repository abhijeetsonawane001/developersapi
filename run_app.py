import os

from app import create_app

config = os.environ.get("APP_CONFIG", "app.config.ProductionConfig")

app = create_app(config=config)

if __name__ == "__main__":
    app.run()
