This directory exposes a ResNet50 model from [`tf.keras.applications`](https://keras.io/api/applications/resnet/#resnet50-function) as a REST API using [FastAPI](https://fastapi.tiangolo.com/).

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

If you want to specify the number of `uvicorn` workers you can do so:

```sh
uvicorn main:app --reload --workers 4
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
$ curl -X POST -F image_file=@cat.jpg http://localhost:8000/predict/image
```

It should output:

```sh
"{\"Label\": \"tabby\", \"Score\": \"0.538\"}"
```

