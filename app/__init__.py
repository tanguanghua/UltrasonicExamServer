import argparse
from flask import Flask
from app.models import connect_db
from app.controllers import register
from config import mapping_config

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--config', type=str, default='wjq-dev', help='Please offer config filename')


def create_app() -> Flask:
    args = parser.parse_args()
    config = args.config

    # 获取实例、加载配置文件
    app = Flask(__name__)

    configure = mapping_config[config]
    app.config.from_object(configure)

    # 连接数据库
    connect_db(app=app)

    # blueprint
    register(app)

    return app
