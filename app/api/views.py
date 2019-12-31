from . import api
import json
from flask import request
from ..utils.evaluate import evaluate_score
from ..models import User, UltrasonicImage
from sqlalchemy.sql import text
from .. import db

def success(result):
    ret = {'status': 1, 'result': result}
    return json.dumps(ret)


def fail(error_string):
    ret = {'status': 0, 'error': error_string}
    return json.dumps(ret)


@api.route('/login', methods=['POST'])
def login():
    data = request.get_data()
    login_info = json.loads(data, encoding='utf-8')

    if 'user_name' not in login_info or 'password' not in login_info:
        return fail('login information is in bad format')

    user = User.query.filter_by(user_name=login_info['user_name']).first()
    if not user:
        return fail(login_info['user_name'] + ' does not exist')

    if user.password != login_info['password']:
        return fail('password is incorrect')
    
    ret = {'id': user.id, 'user_name': user.user_name, 'email': user.email, 'mobile': user.mobile} 
    return success(ret)
    

@api.route('/getExamList')
def getExamList():
    # only select part of the information
    images = db.session.query(UltrasonicImage.id, UltrasonicImage.image_path).order_by(text('rand()')).limit(3)
    # print(images)
    # images = UltrasonicImage.query.order_by(text('rand()')).limit(3)
    exam_list = []
    for image in images:
        exam = {'id': image.id, 'image_path': image.image_path}
        exam_list.append(exam)
    # exam_list = [{'id': 1, 'image_path': 'static/test1.jpg'}, {'id': 2, 'image_path': 'static/test2.jpg'}, {'id': 3, 'image_path': 'static/test3.jpg'}]
    return success(exam_list)


@api.route('/checkExamResult', methods=['POST'])
def checkExamResult():
    data = request.get_data()
    annotations = json.loads(data, encoding='utf-8')
    # print(annotations)

    results = []
    for anno in annotations:
        image = UltrasonicImage.query.filter_by(id=anno['id']).first()
        if not image:
            return fail('no image with id = ' + str(anno['id']))

        
        # anno_user = anno['annotations']
        anno_gt = json.loads(image.annotations, encoding='utf-8')
       
        # if not image or not image.annotations
        avg_score, score_desc = evaluate_score(anno, anno_gt)
        results.append({'id': anno['id'], 'score': avg_score, 'score_desc': score_desc, 'annotations': image.annotations}) 

    print(results)
    return success(results)