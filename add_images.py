import os
from app import create_app
from app.models import db
from app.models.models import UltrasonicImage
import json


def add_images(image_path):
    image_path = os.path.abspath(image_path)
    if not os.path.exists(image_path):
        print('image path does not exist: ' + image_path)
        return

    # whether is the same as the server
    server_root = os.path.dirname(os.path.abspath(__name__))
    server_root = os.path.join(server_root, 'app')
    if not image_path.startswith(server_root):
        print("Please copy the images to the server path: " + server_root)
        return

    prefix = image_path[len(server_root):]
    prefix = prefix.replace('\\', '/')
    images = add_images_impl(image_path, prefix)

    # add to the db
    for image in images:
        db.session.add(image)
    # db.session.add_all(images)
    try:
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print(ex)


def add_images_impl(image_path, prefix):
    total_images = []
    # add to the db
    anno_path = os.path.join(image_path, 'annotations.json')
    if os.path.exists(anno_path):
        with open(anno_path, encoding='utf-8') as fs:
            anno_json = json.load(fs)
            total_images = load_from_json(anno_json, image_path, prefix)
    else:
        for file in os.listdir(image_path):
            path = os.path.join(image_path, file)
            if os.path.isdir(path):
                # relative path
                images = add_images_impl(path, prefix + '/' + file)
                total_images.extend(images)

    return total_images


def load_from_json(anno_json, root_path, prefix):
    if 'annotations' not in anno_json:
        return []

    images = []
    for image_name, annos in anno_json['annotations'].items():
        path = os.path.join(root_path, image_name)
        if not os.path.exists(path):
            print('image does not exist: ' + path)
            continue

        iamge = UltrasonicImage(image_path=prefix + '/' + image_name,
                                body_part=annos['bodyPart'],
                                annotations=json.dumps(annos))

        images.append(iamge)

    return images


if __name__ == "__main__":
    app = create_app('dev')

    image_path = r'G:\MyProject\UltrasonicProject\UltasonicExam\UltrasonicExamServer\app\static\黄文兰   22周    12月1号'
    with app.app_context() as app_ctx:
        add_images(image_path)
