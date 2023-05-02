import os

import cv2
import numpy as np
import torch
from torchvision import transforms

from models.emonet import EmoNet
from src.utils import encode_frame

EMOTIONS = ["Neutral", "Happy", "Sad", "Surprise", "Fear", "Disgust", "Anger", "Contempt"]
n_expression = 8
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
face_detector = cv2.dnn.readNetFromCaffe(os.path.join("models", 'deploy.prototxt'),
                                         os.path.join("models", 'res10_300x300_ssd_iter_140000.caffemodel'))

if device == "cuda":
    face_detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    face_detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

state_dict = torch.load(f"models/emonet_{n_expression}.pth", map_location='cpu')
state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}
net = EmoNet(n_expression=n_expression).to(device)
net.load_state_dict(state_dict, strict=False)
net.eval()


def crop_face(img, bb, square=True):
    (x1, y1, x2, y2) = bb
    if not square:
        return img[y1:y2, x1:x2]
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)
    size = max(x2 - x1, y2 - y1)
    x1 = max(int(cx - size / 2), 0)
    x2 = x1 + size
    y1 = max(int(cy - size / 2), 0)
    y2 = y1 + size
    return img[y1:y2, x1:x2]
    # return cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)


def detect_face(image, min_confidence=0.95):
    h, w = image.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 117.0, 123.0))
    face_detector.setInput(blob)
    detections = face_detector.forward()[0][0]

    best_face = detections[0]
    is_face = best_face[1]
    confidence = best_face[2]
    if not (is_face and confidence >= min_confidence):
        return
    bb = best_face[3: 7] * np.array([w, h, w, h])
    face = crop_face(image, bb=bb.astype("int"))
    face = cv2.resize(face, (256, 256))
    return face


def clean_face(face):
    face = cv2.resize(face, (256, 256))
    face = np.ascontiguousarray(face)
    transform_image = transforms.Compose([transforms.ToTensor()])
    face = transform_image(face).to(device)
    return face


def get_landmarks_from_heatmap(heatmap, shape):
    landmarks = []
    w, h = shape
    for i in range(heatmap.shape[0]):
        split = heatmap[i, :, :]
        max_index = np.argmax(split, axis=None)
        y, x = np.unravel_index(max_index, split.shape)
        x = int(x * w / 64)
        y = int(y * h / 64)
        landmarks.append((x, y))
    return np.array(landmarks)


def analyze_face(face: np.ndarray, keep_landmarks=False, keep_face=False) -> dict:
    face = clean_face(face)
    data = dict()
    with torch.no_grad():
        out = net(face.unsqueeze(0))
        expr = torch.softmax(out["expression"], dim=1)
        data["emotions"] = dict(zip(EMOTIONS, expr[0].tolist()))
        data["valence"] = out["valence"].item()
        data["arousal"] = out["arousal"].item()
        if keep_landmarks:
            heatmap = np.array(out["heatmap"].cpu())[0]
            data["landmarks"] = get_landmarks_from_heatmap(heatmap, face.shape[1:])
        if keep_face:
            data["face"] = np.array(face.transpose(0, 2).transpose(0, 1).cpu())
    return data


def analyze_faces_batch(faces):
    faces = [
        clean_face(face) for face in faces
    ]
    data = dict()
    with torch.no_grad():
        out = net(faces)


def track_eyes(gaze_tracker, face, landmarks, annotate_face=True):
    gaze_tracker.refresh(face, landmarks)
    if annotate_face:
        face = gaze_tracker.annotated_frame()
    data = dict()
    if gaze_tracker.pupils_located:
        data["blinking"] = "Blinking" if gaze_tracker.is_blinking() else ""
        if gaze_tracker.is_left():
            data["looking"] = "Looking LEFT"
        elif gaze_tracker.is_right():
            data["looking"] = "Looking RIGHT"
        elif gaze_tracker.is_center():
            data["looking"] = "Looking CENTER"
        lx, ly = gaze_tracker.pupil_left_coords()
        rx, ry = gaze_tracker.pupil_right_coords()
        data["pupils"] = f"Left pupil at ({lx}, {ly})\t\tRight pupil at ({rx}, {ry})"
    else:
        data["looking"] = ""
        data["left_pupil"] = data["right_pupil"] = "No pupil detected"
        data["blinking"] = ""
    return data, face


def facial_analysis_pipeline(gaze_tracker, image, encode_img=True):
    data = dict()
    face = detect_face(image)
    if face is None:
        return data
    data["face_img"] = encode_frame(face) if encode_img else face
    analysis = analyze_face(face[:, :, ::-1], keep_face=False, keep_landmarks=True)  # correct colors
    eye_data, face = track_eyes(gaze_tracker, face, analysis.pop("landmarks"))
    data.update(analysis)
    data.update(eye_data)
    return data
