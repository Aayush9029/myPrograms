'''
what's happening in this file?

So this program goes to a paticular directory looks for all the sub folders in that directory (grabs the name of the folders and the video file that is inside the folder)
then extracts images from the video (every 5 frames)
extracts face data from the given frame using pretrained face detection model
then trains a pretrained face identification model and labels them with names of the folder
and stores the trained (pickle file aka .pkl file), temp images (extracted faces) in folders respectively



FAQ: why a video?
-> It's easier to take one video rather than taking 1000 images :)
also makes file way more organized.

Why does this file contain complicated and hard to understand code?
-> Because some of the code belong to a library called face_regonition which is a complicated face_rec library which happens to be a bit buggy
so instead of directly using the library i had to edit their source code and make it work with my app.

'''

import os
import cv2
import dlib
import numpy as np
from imutils import face_utils
import tensorflow as tf
import pickle
import onnx
import onnxruntime as ort
from onnx_tf.backend import prepare

os.system("rm -rf faces/training/.DS_Store")   # macos issue (arghh...)
# removing previous temp images (starting from scratch)
os.system("rm -rf faces/tmp")
# making a dir called tmp which got deleted a line ago...
os.system("mkdir faces/tmp")


def area_of(left_top, right_bottom):
    """
    Compute the areas of rectangles given two corners. Math
    """
    hw = np.clip(right_bottom - left_top, 0.0, None)
    return hw[..., 0] * hw[..., 1]


def iou_of(boxes0, boxes1, eps=1e-5):
    """
    Return intersection-over-union (Jaccard index) of boxes.| x[1,2,...] is equivalent to x[1,2,:,:,:] -> source:https://docs.scipy.org/doc/numpy/user/quickstart.html
    """
    overlap_left_top = np.maximum(boxes0[..., :2], boxes1[..., :2])
    overlap_right_bottom = np.minimum(boxes0[..., 2:], boxes1[..., 2:])

    overlap_area = area_of(overlap_left_top, overlap_right_bottom)
    area0 = area_of(boxes0[..., :2], boxes0[..., 2:])
    area1 = area_of(boxes1[..., :2], boxes1[..., 2:])
    return overlap_area / (area0 + area1 - overlap_area + eps)


def hard_nms(box_scores, iou_threshold, top_k=-1, candidate_size=200):
    scores = box_scores[:, -1]
    boxes = box_scores[:, :-1]
    picked = []
    indexes = np.argsort(scores)
    indexes = indexes[-candidate_size:]
    while len(indexes) > 0:
        current = indexes[-1]
        picked.append(current)
        if 0 < top_k == len(picked) or len(indexes) == 1:
            break
        current_box = boxes[current, :]
        indexes = indexes[:-1]
        rest_boxes = boxes[indexes, :]
        iou = iou_of(
            rest_boxes,
            np.expand_dims(current_box, axis=0),
        )
        indexes = indexes[iou <= iou_threshold]

    return box_scores[picked, :]


def predict(width, height, confidences, boxes, prob_threshold, iou_threshold=0.5, top_k=-1):
    """
    Select boxes that contain human faces
    """
    boxes = boxes[0]
    confidences = confidences[0]
    picked_box_probs = []
    picked_labels = []
    for class_index in range(1, confidences.shape[1]):
        probs = confidences[:, class_index]
        mask = probs > prob_threshold
        probs = probs[mask]
        if probs.shape[0] == 0:
            continue
        subset_boxes = boxes[mask, :]
        box_probs = np.concatenate(
            [subset_boxes, probs.reshape(-1, 1)], axis=1)
        box_probs = hard_nms(box_probs,
                             iou_threshold=iou_threshold,
                             top_k=top_k,
                             )
        picked_box_probs.append(box_probs)
        picked_labels.extend([class_index] * box_probs.shape[0])
    if not picked_box_probs:
        return np.array([]), np.array([]), np.array([])
    picked_box_probs = np.concatenate(picked_box_probs)
    picked_box_probs[:, 0] *= width
    picked_box_probs[:, 1] *= height
    picked_box_probs[:, 2] *= width
    picked_box_probs[:, 3] *= height
    return picked_box_probs[:, :4].astype(np.int32), np.array(picked_labels), picked_box_probs[:, 4]


onnx_path = 'models/ultra_light/ultra_light_models/ultra_light_640.onnx'
onnx_model = onnx.load(onnx_path)
predictor = prepare(onnx_model)
ort_session = ort.InferenceSession(onnx_path)
input_name = ort_session.get_inputs()[0].name

shape_predictor = dlib.shape_predictor(
    'models/facial_landmarks/shape_predictor_5_face_landmarks.dat')
fa = face_utils.facealigner.FaceAligner(
    shape_predictor, desiredFaceWidth=112, desiredLeftEye=(0.3, 0.3))


TRAINING_BASE = 'faces/training/'

dirs = os.listdir(TRAINING_BASE)
images = []
names = []

for label in dirs:
    for i, fn in enumerate(os.listdir(os.path.join(TRAINING_BASE, label))):
        print(f"start collecting faces from {label}'s data")
        cap = cv2.VideoCapture(os.path.join(TRAINING_BASE, label, fn))
        frame_count = 0
        while True:
            # read video frame
            ret, raw_img = cap.read()
            # process every 5 frames
            if frame_count % 5 == 0 and raw_img is not None:
                h, w, _ = raw_img.shape
                img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (640, 480))
                img_mean = np.array([127, 127, 127])
                img = (img - img_mean) / 128
                img = np.transpose(img, [2, 0, 1])
                img = np.expand_dims(img, axis=0)
                img = img.astype(np.float32)

                confidences, boxes = ort_session.run(None, {input_name: img})
                boxes, labels, probs = predict(w, h, confidences, boxes, 0.7)

                # if face detected
                if boxes.shape[0] > 0:
                    x1, y1, x2, y2 = boxes[0, :]
                    gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
                    aligned_face = fa.align(raw_img, gray, dlib.rectangle(
                        left=x1, top=y1, right=x2, bottom=y2))
                    aligned_face = cv2.resize(aligned_face, (112, 112))

                    cv2.imwrite(
                        f'faces/tmp/{label}_{frame_count}.jpg', aligned_face)

                    aligned_face = aligned_face - 127.5
                    aligned_face = aligned_face * 0.0078125
                    images.append(aligned_face)
                    names.append(label)

            frame_count += 1
            if frame_count == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                break

with tf.Graph().as_default():
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph('models/mfn/m1/mfn.ckpt.meta')
        saver.restore(sess, 'models/mfn/m1/mfn.ckpt')

        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

        feed_dict = {images_placeholder: images,
                     phase_train_placeholder: False}
        embeds = sess.run(embeddings, feed_dict=feed_dict)
        with open("embeddings/embeddings.pkl", "wb") as f:
            pickle.dump((embeds, names), f)
        print("Done!")
