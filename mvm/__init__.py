
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from mvm.config import DevelopmentConfig
from flask_babel import Babel
from flask_migrate import Migrate
import boto3
import logging



mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
babel = Babel()
loginmanager = LoginManager()
loginmanager.login_view ='users.login'
loginmanager.login_message = 'info'
migrate = Migrate()

rekognition = boto3.client('rekognition', region_name='eu-central-1')



def create_app(config_class=DevelopmentConfig):
    application = Flask(__name__)
    application.config.from_object(config_class)
    
    mail.init_app(application)
    db.init_app(application)
    bcrypt.init_app(application)
    babel.init_app(application)
    loginmanager.init_app(application)
    migrate.init_app(application, db)
    
    application.logger_name = "mvmlogger"
    file_handler = logging.FileHandler(application.config["LOG_FILE"])
    file_handler.setLevel(application.config["LOG_LEVEL"])
    formatter = logging.Formatter(application.config["LOG_FORMAT"])
    file_handler.setFormatter(formatter)
    errorfile_handler = logging.FileHandler(application.config["ERROR_FILE"])
    errorfile_handler.setLevel(logging.ERROR)
    errorfile_handler.setFormatter(formatter)    
    application.logger.setLevel(application.config["LOG_LEVEL"])
    application.logger.addHandler(file_handler)
    application.logger.addHandler(errorfile_handler)

    
    
    from mvm.users.routes import users
    from mvm.items.routes import items
    from mvm.main.routes import main 
    from mvm.errors.handlers import errors
    from mvm.analytics.routes import analytics
    
    application.register_blueprint(users)
    application.register_blueprint(items)
    application.register_blueprint(main)
    application.register_blueprint(errors)
    application.register_blueprint(analytics)
    
    return application

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'].keys())