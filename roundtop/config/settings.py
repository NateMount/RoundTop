# [Settings - Config]

class BaseConfig():
    LOGGING:bool = False
    TESTING:bool = False
    DEBUG:bool = False
    SECRET:str = 'my_secret'
    JWT_AUTH:str = "auth_key"

class DevConfig(BaseConfig):
    FLASK_ENV:str = 'development'
    DB_URI:str = 'sqlite:///roundtop.dev.db'
    DEBUG:bool = True

class ProductionConfig(BaseConfig):
    FLASK_ENV:str = 'production'
    DB_URI:str = 'sqlite:///roundtop.db'
    LOGGING:bool = True

class TestConfig(BaseConfig):
    FLASK_ENV:str = 'development'
    DB_URI:str = 'sqlite:///roundtop.test.db'
    TESTING:bool = True
    DEBUG:bool = True
