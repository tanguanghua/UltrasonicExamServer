from flask import request, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from app.models.exam import get_exam_detail, post_exam
from app.type.exam import TCheckExamResult
from app.utils.auth import Permission, auth_require
from app.utils.warp import success, fail

exam_page = Blueprint('exam', __name__, url_prefix='/exam')


@exam_page.route('/getExamList', methods=['GET'])
@auth_require(Permission.ROOT | Permission.ADMIN | Permission.USER)
def get_exam_list():
    args = request.args
    limit = args.get('limit')
    if limit is not None:
        limit = int(limit)
    else:
        limit = 10

    try:
        exam_list = get_exam_detail(limit)
        return success(exam_list)
    except SQLAlchemyError as e:
        fail(e.args[0])


@exam_page.route('/checkExamResult', methods=['POST'])
@auth_require(Permission.USER)
def check_exam_result():
    data = request.json

    try:
        t_data = TCheckExamResult(**data)
        user_id = t_data.user_id
        annotations = t_data.annotations
        results = post_exam(annotations, user_id)
        return success(results)
    except ValidationError:
        return fail('Params error')
    except SQLAlchemyError as e:
        fail(e.args[0])
