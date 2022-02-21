"""
Adapted from:

(1) https://github.com/shanesoh/deploy-ml-fastapi-redis-docker/
(2) https://github.com/aniketmaurya/tensorflow-fastapi-starter-pack
"""

import onnxruntime as ort
import json

from fastapi import FastAPI, File, HTTPException
from utils import prepare_image, decode_predictions


app = FastAPI(title="ONNX image classification API")


@app.get("/")
async def home():
    return "Welcome!"


@app.on_event("startup")
def load_modules():
    global resnet_model_sess
    resnet_model_sess = ort.InferenceSession("resnet50_w_preprocessing.onnx")

    global imagenet_categories
    with open("imagenet_classes.txt", "r") as f:
        imagenet_categories = [s.strip() for s in f.readlines()]


@app.post("/predict/image")
async def predict_api(image_file: bytes = File(...)):

    image = prepare_image(image_file)

    if len(image.shape) != 4:
        raise HTTPException(
            status_code=400, detail="Only 3-channel RGB images are supported."
        )

    predictions = resnet_model_sess.run(None, {"image_input": image})[0]
    response_dict = decode_predictions(predictions, imagenet_categories)

    return json.dumps(response_dict)
