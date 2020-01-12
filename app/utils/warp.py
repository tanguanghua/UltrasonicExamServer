from flask import jsonify


def success(result):
    ret = {'status': 1, 'result': result}
    return jsonify(ret)


def fail(error_string):
    ret = {'status': 0, 'error': error_string}
    return jsonify(ret)
