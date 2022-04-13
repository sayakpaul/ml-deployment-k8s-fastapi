import io
from typing import Dict, List

import numpy as np
from fastapi import HTTPException
from PIL import Image

TARGET_IMG_WIDTH = 224
TARGET_IMG_HEIGHT = 224

def raise_http_exception():
    """Raise HTTPException with the status code 400"""
    raise HTTPException(
        status_code=400, detail="Supported formats are JPEG, JPG, and PNG."
    )

def prepare_image(image_file: bytes, with_resizing: bool=False) -> np.ndarray:
    """Prepares an image for model prediction."""
    image = Image.open(io.BytesIO(image_file))
    width, height = image.size

    if image.format not in ["JPEG", "JPG", "PNG"] :
        raise_http_exception()

    if with_resizing is True:
        image = image.resize((TARGET_IMG_WIDTH, TARGET_IMG_HEIGHT))
    else:
        if width is not TARGET_IMG_WIDTH or \
            height is not TARGET_IMG_HEIGHT:
            raise_http_exception()

    image = np.array(image).astype("float32")
    return np.expand_dims(image, 0)

def decode_predictions(
    predictions: np.ndarray, imagenet_categories: List[str]
) -> Dict[str, float]:
    """Decodes model predictions."""
    predictions = np.squeeze(predictions)
    pred_name = imagenet_categories[int(predictions.argmax())]
    response_dict = {"Label": pred_name, "Score": f"{predictions.max():.3f}"}

    return response_dict        