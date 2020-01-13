import os
import pathlib
import importlib
from flask import Flask


def register(app: Flask):
    root = pathlib.Path(__file__).parent
    files = os.listdir(root)

    for item in files:
        path = str(pathlib.Path.joinpath(root, item))
        if not os.path.isdir(path) and path != __file__:
            temp = item.split('.')[0]
            module = importlib.import_module(f'app.controllers.{temp}')
            auto_blueprint = module.__dict__[f'{temp}_page']
            app.register_blueprint(auto_blueprint)
