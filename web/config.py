import os
try:
    from web.keys import username, password
except ImportError:
    username = ""
    password = ""

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://" + username + ":" + password + "@test-db-instance.cnv6hbuo38a0.us-east-1.rds.amazonaws.com:3306/foodbuddies"
    SECRET_KEY = os.getenv('SECRET_KEY')

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = 'test!'

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig
)

key = Config.SECRET_KEY
