This directory exposes the ONNX model we converted in [this notebook](https://github.com/sayakpaul/ml-deployment-k8s-fastapi/blob/main/notebooks/TF_to_ONNX.ipynb) as a REST API using [FastAPI](https://fastapi.tiangolo.com/).

## Setup 

Install the dependencies:

```sh
$ pip install -r requirements.txt
```

Download a test image:

```sh
$ wget http://images.cocodataset.org/val2017/000000039769.jpg -O cat.jpg
```

## Deploy locally

```sh
$ uvicorn main:app --reload
```

It should show something like so:

```sh
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [79147] using statreload
INFO:     Started server process [79149]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Note the port number and run a request:

```sh
$ curl -X POST -F image_file=@cat.jpg -F with_resize=True -F with_post_process=True http://localhost:8000/predict/image
```

It should output:

```sh
"{\"Label\": \"tabby\", \"Score\": \"0.538\"}"
```

### Client request code in Python

```python
import requests

url = "http://localhost:8000/predict/image"
payload = {"with_resize": True, "with_post_process": True}
files = {"image_file": open("cat.jpg", "rb")}

resp = requests.post(url=url, data=payload, files=files)
print(resp.json())
```
