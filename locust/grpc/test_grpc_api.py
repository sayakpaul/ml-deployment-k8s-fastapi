import numpy as np
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

import grpc

image = tf.image.decode_jpeg(tf.io.read_file("../cat.jpg"))
image = tf.image.resize(image, (224, 224))[None, ...]

channel = grpc.insecure_channel("34.135.245.34:8500")
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)


request = predict_pb2.PredictRequest()
request.model_spec.name = "resnet"
request.model_spec.signature_name = "serving_default"
request.inputs["image_input"].CopyFrom(tf.make_tensor_proto(image))

grpc_predictions = stub.Predict(request, 25.0)

grpc_predictions = grpc_predictions.outputs["resnet50"].float_val
grpc_predictions = np.array(grpc_predictions).reshape(len(image), -1)
print("Prediction class: {}".format(np.argmax(grpc_predictions, axis=-1)))
