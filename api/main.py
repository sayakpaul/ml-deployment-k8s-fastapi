import json
import os
import tarfile
import urllib.request

import tensorflow as tf
from fastapi import FastAPI, File, HTTPException

from utils import decode_predictions, prepare_image

app = FastAPI(title="TensorFlow image classification API")


@app.get("/")
async def home():
    return "Welcome!"


@app.on_event("startup")
def load_modules():
    model_filename = "resnet50_w_preprocessing_tf.tar.gz"
    model_foldername = model_filename.split(".")[0]
    model_url = f"https://github.com/sayakpaul/ml-deployment-k8s-fastapi/releases/download/v1.0.0/{model_filename}"

    if not os.path.exists(model_filename):
        urllib.request.urlretrieve(model_url, model_filename)

    if not os.path.exists(model_foldername):
        with tarfile.open(model_filename) as fp:
            fp.extractall(model_foldername)

    global model
    model = tf.keras.models.load_model(f"{model_foldername}/{model_foldername}")

    category_filename = "imagenet_classes.txt"
    category_url = f"https://raw.githubusercontent.com/pytorch/hub/master/{category_filename}"
    urllib.request.urlretrieve(category_url, category_filename)

    global imagenet_categories
    with open(category_filename, "r") as f:
        imagenet_categories = [s.strip() for s in f.readlines()]


@app.post("/predict/image")
async def predict_api(image_file: bytes = File(...)):

    image = prepare_image(image_file)

    if len(image.shape) != 4:
        raise HTTPException(
            status_code=400, detail="Only 3-channel RGB images are supported."
        )

    predictions = model.predict(image)
    response_dict = decode_predictions(predictions, imagenet_categories)

    return json.dumps(response_dict)
