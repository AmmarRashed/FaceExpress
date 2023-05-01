import pickle
from argparse import ArgumentParser

import pandas as pd
from imutils.video import FileVideoStream
from tqdm import tqdm

from src.facial_analysis import *

parser = ArgumentParser()
parser.add_argument("path")
parser.add_argument("--progress", action="store_true", help="Show progress bar")
parser.add_argument("--as_tsv", action="store_true", help="Save as a dataframe")
parser.add_argument("--batch_size", help="Batch size", default=128, type=int)
parser.add_argument("--conf", help="Face detection confidence threshold (int 0-100)", default=97, type=int)
args = parser.parse_args()

video = FileVideoStream(args.path).start()

frame_idx = []
results = {"Emotions": [], "Valence": [], "Arousal": []}


def process_batch(faces):
    global results
    with torch.no_grad():
        out = net(faces)
        expr = torch.softmax(out["expression"], dim=-1)
        results["Emotions"].append(expr)
        results["Valence"].append(out["valence"])
        results["Arousal"].append(out["arousal"])


def loop(progress=False):
    global frame_idx
    faces = []
    i = 0
    while True:
        frame = video.read()
        if frame is None:
            break
        face = detect_face(frame, min_confidence=int(args.conf) / 100)
        if face is not None:
            faces.append(clean_face(face))
            frame_idx.append(i)
            if len(faces) == int(args.batch_size):
                process_batch(torch.stack(faces))
                faces = []
        i += 1
        if progress:
            pbar.update(1)
    if len(faces):
        process_batch(torch.stack(faces))


if args.progress:
    with tqdm() as pbar:
        loop(progress=True)
else:
    loop(progress=False)

for k, v in results.items():
    results[k] = np.array(torch.cat(v).cpu())
results["Frame Index"] = frame_idx

output_path = '.'.join(args.path.split(".")[:-1])

if args.as_tsv:
    last_frame = max(results["Frame Index"])
    df = pd.DataFrame(index=pd.RangeIndex(last_frame + 1), columns=["valence", "arousal"] + EMOTIONS)
    idx = results["Frame Index"]
    df["valence"].loc[idx] = results["Valence"]
    df["arousal"].loc[idx] = results["Arousal"]
    for i, e in enumerate(EMOTIONS):
        df[e].loc[idx] = results["Emotions"][:, i]
    df = df.reset_index().rename(columns={"index": "frame"})

    df.to_csv(output_path + ".tsv", sep="\t", index=False)
    print("Saved")

else:
    pickle.dump(results, open(output_path + ".pkl", "wb"))
