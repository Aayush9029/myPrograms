'''
what is happening in this file?

Basically takes all the cascade data (face feattures) data which is a out put of train.py and analyses it 
finds faces in the live video and sends it to the database.

zzz

'''
from firebase import firebase
import time
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


studentNumber = {
    "Aayush": 927409,
    "Mahim": 78278,
    "Eesa": 596262,
    "Timmy": 592619,
    "Areeb": 693371
}


def PostToFirebase(name, time):
    global studentNumber
    firebase1 = firebase.FirebaseApplication(
        "https://assistant-tomoya.firebaseio.com/", None)
    if name in studentNumber:
        data = {
            "Name": name,
            "Student_Number": studentNumber[name],
            "Time": time
        }
    else:
        data = {
            "Name": name,
            "Student_Number": 0,  # default is 0
            "Time": time
        }
    result = firebase1.post("/Attendance/", data)
    print(result)
    print(f"posted {name} at time {time}")


last_person = ''  # this holds name_value for last person

studentsSeen = []  # this holds name in database temporarily


''' Not sure how OOP will be handy will have to pass this time'''
# class Student:
#     def __init__(self, name, time=1):
#         self.name = name
#         self.time = str(time)

#     def sendToDatabase(self):
#         print(self.name, self.time)


def sendNames(names):
    global studentsSeen
    if names not in studentsSeen and names != 'unknown':
        studentsSeen.append(names)
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        # print(current_time)
        print("FACE DETECTED:", names, current_time)
        PostToFirebase(names, current_time)


def area_of(left_top, right_bottom):
    """
    Compute the areas of rectangles given two corners.
    For visual purposes only
    """
    hw = np.clip(right_bottom - left_top, 0.0, None)
    return hw[..., 0] * hw[..., 1]


def iou_of(boxes0, boxes1, eps=1e-5):
    """
    Return intersection-over-union of boxes.
    source: stackoverflow.com
    """
    overlap_left_top = np.maximum(boxes0[..., :2], boxes1[..., :2])
    overlap_right_bottom = np.minimum(boxes0[..., 2:], boxes1[..., 2:])

    overlap_area = area_of(overlap_left_top, overlap_right_bottom)
    area0 = area_of(boxes0[..., :2], boxes0[..., 2:])
    area1 = area_of(boxes1[..., :2], boxes1[..., 2:])
    return overlap_area / (area0 + area1 - overlap_area + eps)


def hard_nms(box_scores, iou_threshold, top_k=-1, candidate_size=200):
    """
    Perform hard non-maximum-supression to filter out boxes with iou greater
    than threshold

    half of the code: stackoverflow.com
    """
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

    source: opencv, numpy and face_recognition (github)
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


# this is a pre-tranied model (makes traning a bit easier and requires lot less images)
onnx_path = 'models/ultra_light/ultra_light_models/ultra_light_640.onnx'
onnx_model = onnx.load(onnx_path)
predictor = prepare(onnx_model)
ort_session = ort.InferenceSession(onnx_path)
input_name = ort_session.get_inputs()[0].name

shape_predictor = dlib.shape_predictor(
    'models/facial_landmarks/shape_predictor_5_face_landmarks.dat')
fa = face_utils.facealigner.FaceAligner(
    shape_predictor, desiredFaceWidth=112, desiredLeftEye=(0.3, 0.3))

threshold = 0.63

# load distance
with open("embeddings/embeddings.pkl", "rb") as f:
    (saved_embeds, names) = pickle.load(f)


with tf.Graph().as_default():
    '''
    some code belongs to tensorflow and opencv-python (pip)
    '''
    with tf.Session() as sess:

        saver = tf.train.import_meta_graph('models/mfn/m1/mfn.ckpt.meta')
        saver.restore(sess, 'models/mfn/m1/mfn.ckpt')

        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        embedding_size = embeddings.get_shape()[1]

        video_capture = cv2.VideoCapture(0)

        while True:
            fps = video_capture.get(cv2.CAP_PROP_FPS)
            ret, frame = video_capture.read()

            # preprocess faces
            h, w, _ = frame.shape
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (640, 480))
            img_mean = np.array([127, 127, 127])
            img = (img - img_mean) / 128
            img = np.transpose(img, [2, 0, 1])
            img = np.expand_dims(img, axis=0)
            img = img.astype(np.float32)

            # detect faces
            confidences, boxes = ort_session.run(None, {input_name: img})
            boxes, labels, probs = predict(w, h, confidences, boxes, 0.7)

            # locate faces
            faces = []
            boxes[boxes < 0] = 0
            for i in range(boxes.shape[0]):
                box = boxes[i, :]
                x1, y1, x2, y2 = box

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                aligned_face = fa.align(frame, gray, dlib.rectangle(
                    left=x1, top=y1, right=x2, bottom=y2))
                aligned_face = cv2.resize(aligned_face, (112, 112))

                aligned_face = aligned_face - 127.5
                aligned_face = aligned_face * 0.0078125

                faces.append(aligned_face)

            # face embedding
            if len(faces) > 0:
                predictions = []

                faces = np.array(faces)
                feed_dict = {images_placeholder: faces,
                             phase_train_placeholder: False}
                embeds = sess.run(embeddings, feed_dict=feed_dict)

                # prediciton using distance
                for embedding in embeds:
                    diff = np.subtract(saved_embeds, embedding)
                    dist = np.sum(np.square(diff), 1)
                    idx = np.argmin(dist)
                    if dist[idx] < threshold:
                        predictions.append(names[idx])
                    else:
                        predictions.append("unknown")

                # draw
                for i in range(boxes.shape[0]):
                    box = boxes[i, :]

                    text = f"{predictions[i]}"
                    if last_person != text:  # this function prints people names
                        # print(text)
                        sendNames(text)
                        last_person = text

                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 18, 236), 2)
                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (x1, y2 - 20), (x2, y2),
                                  (80, 18, 236), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, text, (x1 + 6, y2 - 6),
                                font, 0.3, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
