import base64

import cv2


def encode_frame(frame):
    ret, buffer = cv2.imencode('.jpg', frame)
    frame_str = base64.b64encode(buffer).decode('utf-8')
    return frame_str


def draw_face_box(frame, region, crop=True):
    x1, y1, w, h = region["x"], region["y"], region["w"], region["h"]
    x2, y2 = x1 + w, y1 + h
    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    if crop:
        face = frame[y1:y2, x1:x2]
        return frame, face
    return frame
