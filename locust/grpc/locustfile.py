"""Launch a load-test with Locust for the gRPC API.

Code copied and modified from here: 
http://docs.locust.io/en/stable/testing-other-systems.html
"""


import numpy as np
import tensorflow as tf
from locust import User, task
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

import grpc

# Patch grpc so that it uses gevent instead of asyncio
import grpc.experimental.gevent as grpc_gevent

grpc_gevent.init_gevent()


class ImgClssificationUser(User):
    def __init__(self, environment):
        super().__init__(environment)
        self.channel = grpc.insecure_channel("34.135.245.34:8500")
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(
            self.channel
        )
        self.request = predict_pb2.PredictRequest()
        self.request.model_spec.name = "resnet"
        self.request.model_spec.signature_name = "serving_default"

    def prepare_img(self):
        image = tf.image.decode_jpeg(tf.io.read_file("../cat.jpg"))
        image = tf.image.resize(image, (224, 224))[None, ...]
        return image

    @task
    def predict(self):
        sample_image = self.prepare_img()

        self.request.inputs["image_input"].CopyFrom(
            tf.make_tensor_proto(sample_image)
        )
        preds = self.stub.Predict(self.request, 30.0)

        # Uncomment to debug.
        # preds = preds.outputs["resnet50"].float_val
        # preds = np.array(preds).reshape(1, -1)
        # print("Prediction class: {}".format(np.argmax(preds, axis=-1)))
