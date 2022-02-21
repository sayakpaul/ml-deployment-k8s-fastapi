FROM python:3.8

WORKDIR /app

# install dependencies
COPY ./api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# download ONNX model and classes.txt
RUN wget https://github.com/sayakpaul/ml-deployment-k8s-fastapi/releases/download/v1.0.0/resnet50_w_preprocessing.onnx -O resnet50_w_preprocessing.onnx
RUN wget https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt -O imagenet_classes.txt

# copy fastAPI app codebase
COPY ./api /app

# run the fastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]