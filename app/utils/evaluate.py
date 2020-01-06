import cv2
import numpy as np
import json


def evaluate_score(anno_user, anno_gt):
    ret_scores = []
    # body part
    if anno_gt['bodyPart'] != anno_user['bodyPart']:
        desc = '身体部位不一致，应为：' + anno_gt['bodyPart']
        ret_scores.append({'part': anno_user['bodyPart'], 'score': 0, 'desc': desc})
        return 0, ret_scores

    # for each annotation
    anno_gt = anno_gt['annotations']
    anno_user = anno_user['annotations']

    # ground truth
    anno_mapping_gt = {}
    for anno in anno_gt:
        anno_name = anno['name']

        if anno_name in anno_mapping_gt.keys():
            anno_mapping_gt[anno_name].append(anno)
        else:
            anno_mapping_gt[anno_name] = [anno]

    # user
    anno_mapping_user = {}
    for anno in anno_user:
        anno_name = anno['name']

        if anno_name in anno_mapping_user.keys():
            anno_mapping_user[anno_name].append(anno)
        else:
            anno_mapping_user[anno_name] = [anno]

    # evaluate
    avg_score = 0
    for sub_type, annos in anno_mapping_gt.items():
        if sub_type not in anno_mapping_user:
            ret_scores.append({'part': sub_type, 'score': 0, 'desc': '未标出结构：' + sub_type})
        else:
            # sub_type='脉络丛'
            # annos = anno_mapping_gt[sub_type]
            # print(sub_type)
            score = iou(annos, anno_mapping_user[sub_type])
            ret_scores.append({'part': sub_type, 'score': score, 'desc': ''})

            avg_score += score

    # structure which does not exist in ground truth
    for sub_type in anno_mapping_user.keys():
        if sub_type not in anno_mapping_gt:
            ret_scores.append({'part': sub_type, 'score': 0, 'desc': '结构不存在：' + sub_type})

    avg_score /= len(ret_scores)
    return avg_score, ret_scores


def iou(anno_user, anno_gt):
    minX = 10000
    maxX = 0
    minY = 10000
    maxY = 0

    # find bounding box
    vertex_gt = []
    for anno in anno_user:
        temp = convertVertex(anno['vertex'])

        # at least 3 points
        if len(temp) > 2:
            vertex_gt.append(temp)

            [minX, minY] = np.min(temp + [[minX, minY]], axis=0)
            [maxX, maxY] = np.max(temp + [[maxX, maxY]], axis=0)

    vertex_user = []
    for anno in anno_gt:
        temp = convertVertex(anno['vertex'])

        # at least 3 points
        if len(temp) > 2:
            vertex_user.append(temp)

            [minX, minY] = np.min(temp + [[minX, minY]], axis=0)
            [maxX, maxY] = np.max(temp + [[maxX, maxY]], axis=0)

    if len(vertex_gt) == 0 or len(vertex_user) == 0:
        return 0

    # draw to bitmap
    width = maxX - minX + 3
    height = maxY - minY + 3

    mask_gt = np.zeros((height, width), np.uint8)
    mask_user = np.zeros((height, width), np.uint8)

    # cv2.fillPoly(mask_gt, np.array([[(10, 10), (100, 10), (100, 100), (10, 100)]]), 1)
    # cv2.imshow('gt', mask_gt.astype(np.float64))
    # cv2.waitKey()

    for vertex in vertex_gt:
        cv2.fillPoly(mask_gt, np.array([vertex]), 1, offset=(-minX + 1, -minY + 1))
    for vertex in vertex_user:
        cv2.fillPoly(mask_user, np.array([vertex]), 1, offset=(-minX + 1, -minY + 1))

    mask_overlap = cv2.bitwise_and(mask_user, mask_gt)

    # cv2.imshow('gt', mask_gt.astype(np.float64))
    # cv2.imshow('user', mask_user.astype(np.float64))
    # cv2.imshow('overlap', mask_overlap.astype(np.float64))

    # cv2.waitKey()

    # iou
    overlap = np.sum(mask_overlap)

    union = np.sum(mask_gt) + np.sum(mask_user) - overlap

    return overlap * 100.0 / union


def convertVertex(anno_vertex):
    vertex_list = anno_vertex.split(';')

    ret_vertex = []
    for vertex in vertex_list:
        x, y = vertex.split(',')
        ret_vertex.append([round(float(x)), round(float(y))])

    return ret_vertex


if __name__ == "__main__":
    path = r'G:\MyProject\UltrasonicProject\UltasonicExam\Server\app\static\five\annotations.json'

    with open(path, encoding='utf-8') as fs:
        anno_json = json.load(fs)

        annotations = anno_json['annotations']
        avg_score, score_desc = evaluate_score(annotations['1.jpg'], annotations['3.jpg'])

        print(score_desc)
        print(avg_score)
