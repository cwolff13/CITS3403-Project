from flask_migrate import Migrate
from app import create_app, db
from app.config import DeploymentConfig, Config

config_setting = DeploymentConfig()
app = create_app(config_setting)

migrate = Migrate(app,db)