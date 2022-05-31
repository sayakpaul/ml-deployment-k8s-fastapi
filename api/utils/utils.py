import io
import json
from typing import Dict, List

import numpy as np
import requests
from fastapi import HTTPException
from github import Github
from PIL import Image

TARGET_IMG_WIDTH = 224
TARGET_IMG_HEIGHT = 224


def get_latest_model_url() -> str:
    """Gets the model download URL from the latest release artifacts."""
    g = Github()

    repo = g.get_repo("sayakpaul/ml-deployment-k8s-fastapi")
    latest_release = repo.get_latest_release()
    assets = list(latest_release.get_assets())

    download_url = None

    for asset in assets:
        if "onnx" in asset.name:
            asset_url = asset.url
            r = requests.get(asset_url)
            response = json.loads(r.text)
            download_url = response["browser_download_url"]

    return download_url


def raise_http_exception(msg):
    """Raise HTTPException with the status code 400"""
    raise HTTPException(status_code=400, detail=msg)


def prepare_image(image_file: bytes, with_resizing: bool = False) -> np.ndarray:
    """Prepares an image for model prediction."""
    image = Image.open(io.BytesIO(image_file))
    width, height = image.size

    if image.format not in ["JPEG", "JPG", "PNG"]:
        raise_http_exception("Supported formats are JPEG, JPG, and PNG.")

    if with_resizing:
        image = image.resize((TARGET_IMG_WIDTH, TARGET_IMG_HEIGHT))
    else:
        if width is not TARGET_IMG_WIDTH or height is not TARGET_IMG_HEIGHT:
            raise_http_exception("Image size is not 224x224")

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
