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
state_dict = torch.load(f"models/emonet_{n_expression}.pth", map_location='cpu')
state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}
net = EmoNet(n_expression=n_expression).to(device)
net.load_state_dict(state_dict)
net.eval()


def detect_face(image, min_confidence=0.95):
    base_img = image.copy()
    original_size = base_img.shape
    target_size = (300, 300)
    image = cv2.resize(image, target_size)
    aspect_ratio_x = (original_size[1] / target_size[1])
    aspect_ratio_y = (original_size[0] / target_size[0])

    blob = cv2.dnn.blobFromImage(image)
    face_detector.setInput(blob)
    detections = face_detector.forward()[0][0]

    best_face = detections[0]
    is_face = best_face[1]
    confidence = best_face[2]
    if not (is_face and confidence >= min_confidence):
        return
    left, top, right, bottom = (best_face[-4:] * 300).astype(int)

    detected_face = base_img[int(top * aspect_ratio_y):int(bottom * aspect_ratio_y),
                    int(left * aspect_ratio_x):int(right * aspect_ratio_x)]
    return detected_face


def analyze_face(image: np.ndarray) -> dict:
    image = cv2.resize(image, (256, 256))
    image = np.ascontiguousarray(image)
    transform_image = transforms.Compose([transforms.ToTensor()])
    image = transform_image(image).to(device)
    data = dict()
    with torch.no_grad():
        out = net(image.unsqueeze(0))
        expr = torch.softmax(out["expression"], dim=1)
        data["emotions"] = dict(zip(EMOTIONS, expr[0].tolist()))
        data["valence"] = out["valence"].item()
        data["arousal"] = out["arousal"].item()
    return data


def facial_analysis_pipeline(image):
    data = dict()
    face = detect_face(image)
    if face is None:
        return data
    data["face_img"] = encode_frame(face)
    analysis = analyze_face(face)
    data.update(analysis)
    return data
