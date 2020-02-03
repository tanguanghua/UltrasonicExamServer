class Config(object):
    DEBUG = False
    NUM_TESTS = 10
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/ultrasonic'


class DevConfig(Config):
    DEBUG = True    
    APP_URL = 'http://127.0.0.1：5000'


class ProConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


mapping_config = {
    'dev': DevConfig,
    'pro': ProConfig
}