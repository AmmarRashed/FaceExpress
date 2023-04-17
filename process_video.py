import pickle
from argparse import ArgumentParser

from imutils.video import FileVideoStream
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.facial_analysis import *
from src.utils import MyDataset

parser = ArgumentParser()
parser.add_argument("path")
parser.add_argument("--progress", action="store_true", help="Show progress bar")
args = parser.parse_args()

video = FileVideoStream(args.path).start()

frame_idx = []
faces = []


def loop(progress=False):
    global frame_idx, faces
    i = 0
    while True:
        frame = video.read()
        if frame is None:
            break
        face = detect_face(frame)
        if face is not None:
            faces.append(clean_face(face))
            frame_idx.append(i)
        
        i += 1
        if progress:
            pbar.update(1)


if args.progress:
    with tqdm() as pbar:
        loop(progress=True)
else:
    loop(progress=False)

results = {"Emotions": [], "Valence": [], "Arousal": []}
faces_dataset = MyDataset(torch.stack(faces))
faces_dataloader = DataLoader(faces_dataset, batch_size=min(32, len(faces_dataset)), shuffle=False)
with torch.no_grad():
    for batch in faces_dataloader:
        out = net(batch)
        expr = torch.softmax(out["expression"], dim=-1)
        results["Emotions"].append(expr)
        results["Valence"].append(out["valence"])
        results["Arousal"].append(out["arousal"])

for k, v in results.items():
    results[k] = np.array(torch.cat(v).cpu())
results["Frame Index"] = frame_idx

output_path = '.'.join(args.path.split(".")[:-1]) + ".pkl"
pickle.dump(results, open(output_path, "wb"))
