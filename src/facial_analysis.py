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
    target_size = (300, 300)
    image = cv2.resize(image, target_size)
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
    return face


def clean_face(face):
    face = cv2.resize(face, (256, 256))
    face = np.ascontiguousarray(face)
    transform_image = transforms.Compose([transforms.ToTensor()])
    face = transform_image(face).to(device)
    return face


def analyze_face(face: np.ndarray, keep_landmarks=False) -> dict:
    face = clean_face(face)
    data = dict()
    with torch.no_grad():
        out = net(face.unsqueeze(0))
        expr = torch.softmax(out["expression"], dim=1)
        data["emotions"] = dict(zip(EMOTIONS, expr[0].tolist()))
        data["valence"] = out["valence"].item()
        data["arousal"] = out["arousal"].item()
        data["heatmap"] = np.array(out["heatmap"].cpu())
    return data


def analyze_faces_batch(faces):
    faces = [
        clean_face(face) for face in faces
    ]
    data = dict()
    with torch.no_grad():
        out = net(faces)


def facial_analysis_pipeline(image, encode_img=True):
    data = dict()
    face = detect_face(image)
    if face is None:
        return data
    data["face_img"] = encode_frame(face) if encode_img else face
    analysis = analyze_face(face[:, :, ::-1])
    data.update(analysis)
    return data
