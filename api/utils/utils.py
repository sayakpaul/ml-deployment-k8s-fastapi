import io
from typing import Dict, List

import numpy as np
from fastapi import HTTPException
from PIL import Image


def prepare_image(image_file: bytes) -> np.ndarray:
    """Prepares an image for model prediction."""
    image = Image.open(io.BytesIO(image_file))

    if image.format in ["JPEG", "JPG", "PNG"]:
        image = np.array(image).astype("float32")
        return np.expand_dims(image, 0)
    else:
        raise HTTPException(
            status_code=400, detail="Supported formats are JPEG, JPG, and PNG."
        )