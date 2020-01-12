import json
from flask import request, Blueprint
from ..utils.evaluate import evaluate_score
from app.models.models import UltrasonicImage, ExamResult
from sqlalchemy.sql import text
from app.models import db
from app.utils.warp import success, fail

views = Blueprint('api', __name__, url_prefix='/api')


@views.route('/getExamList')
def getExamList():
    # only select part of the information
    # print(db.NUM_TESTS)
    images = db.session.query(UltrasonicImage.id, UltrasonicImage.image_path).order_by(text('rand()')).limit(
        db.NUM_TESTS)
    # print(images)
    # images = UltrasonicImage.query.order_by(text('rand()')).limit(3)
    exam_list = []
    for image in images:
        exam = {'id': image.id, 'image_path': image.image_path}
        exam_list.append(exam)
    # exam_list = [{'id': 1, 'image_path': 'static/five/1.jpg'}, {'id': 2, 'image_path': 'static/five/2.jpg'}, {'id': 3, 'image_path': 'static/five/3.jpg'}]
    return success(exam_list)


@views.route('/checkExamResult', methods=['POST'])
def checkExamResult():
    data = request.get_data()
    request_data = json.loads(data, encoding='utf-8')
    # print(annotations)

    user_id = request_data['user_id']

    results = []
    for anno in request_data['annotations']:
        image = UltrasonicImage.query.filter_by(id=anno['id']).first()
        if not image:
            return fail('no image with id = ' + str(anno['id']))

        # anno_user = anno['annotations']
        anno_gt = json.loads(image.annotations, encoding='utf-8')

        # if not image or not image.annotations
        avg_score, score_desc = evaluate_score(anno, anno_gt)
        results.append(
            {'id': anno['id'], 'score': avg_score, 'score_desc': score_desc, 'annotations': image.annotations})

        # insert into table
    exam = ExamResult(user_id=user_id, score=avg_score)
    db.session.add(exam)
    try:
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        return fail(ex.error_string)

    # print(results)
    return success(results)
