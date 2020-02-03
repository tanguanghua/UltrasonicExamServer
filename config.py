class Config(object):
    DEBUG = False
    NUM_TESTS = 10
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/ultrasonic'


class DevConfig(Config):
    DEBUG = True
    APP_URL = 'http://127.0.0.1:5000'


class WjqConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://thy:wJLa57iMAdMDjZXx@101.37.27.57/thy'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


mapping_config = {
    'dev': DevConfig,
    'wjq-dev': WjqConfig,
    'pro': ProConfig
}
