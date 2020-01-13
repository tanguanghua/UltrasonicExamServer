import json
from typing import Sequence
from sqlalchemy.sql.functions import random
from app.models import db, session_commit
from app.models.models import UltrasonicImage, ExamResult
from app.type.exam import TAnnotation
from app.utils.evaluate import evaluate_score


def get_exam_detail(limit: int) -> Sequence[object]:
    images = db.session. \
        query(UltrasonicImage.id, UltrasonicImage.image_path). \
        order_by(random()). \
        limit(limit).all()

    exam_list = []
    for image in images:
        exam = {
            'id': image.id,
            'image_path': image.image_path
        }
        exam_list.append(exam)
    return exam_list


def post_exam(annotations: Sequence[TAnnotation], user_id: int) -> list:
    results = []
    for annotation in annotations:
        image = UltrasonicImage.query.filter_by(id=annotation.id).first()
        if not image:
            raise RuntimeError(f'no image with id = {annotation.id}')

        annotation_gt = json.loads(image.annotations, encoding='utf-8')
        temp = json.loads(annotation.json(), encoding='utf-8')

        avg_score, score_desc = evaluate_score(temp, annotation_gt)
        results.append({
            'id': annotation.id,
            'score': avg_score,
            'score_desc': score_desc,
            'annotations': image.annotations
        })

    exam = ExamResult(user_id=user_id, score=avg_score)
    db.session.add(exam)
    session_commit()

    return results


if __name__ == '__main__':
    from app import create_app

    app = create_app()
    with app.app_context():
        get_exam_detail(10)
