
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import os
from kraken import binarization, rpred, pageseg, serialization, lib

def _bytes_to_pil(img_bytes: bytes) -> Image.Image:
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)

def preprocess_for_camera(img: Image.Image) -> Image.Image:
    # Convert to grayscale and binarize with kraken's adaptive method
    return binarization.nlbin(img)

def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Kraken model not found: {path}")
    return serialization.load_any(path)

def predict_lines(img_bytes: bytes, model_path: str):
    pil = _bytes_to_pil(img_bytes)
    pil = preprocess_for_camera(pil)
    # Segment lines
    seg = pageseg.segment(pil)
    # Recognize
    model = load_model(model_path)
    preds = rpred.rpred(model, pil, seg)
    lines = []
    for l in preds:
        text = l.prediction
        # crop the line region
        x1,y1,x2,y2 = l.bounds
        crop = pil.crop((x1,y1,x2,y2))
        output = BytesIO()
        crop.save(output, format="PNG")
        lines.append({"text": text, "crop": output.getvalue()})
    return lines

def train_model(base_model: str, output_path: str, training_pairs: list[tuple[str, str]]):
    """
    training_pairs: list of (image_path, label_path) pairs in kraken ALTO/SEG format.
    For simplicity, this scaffold assumes we wrote single-line snippets and labels to temp files.
    """
    # Minimal CLI-style training interface. In production, switch to proper GT formats.
    from kraken import blla, training
    # This is a placeholder hook: real kraken training expects PAGE-XML/ALTO or line-level markdown.
    # Here we just forward to kraken.training with a simple dataset. User can replace with their pipeline.
    training.train(base_model, output_path, training_pairs)
    return output_path
