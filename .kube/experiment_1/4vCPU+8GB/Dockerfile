FROM python:3.8

WORKDIR /app

# install dependencies
COPY ./.kube/experiment_1/4vCPU+8GB/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy fastAPI app codebase
COPY ./api /app

# run the fastAPI app
CMD ["gunicorn", "main:app", "--workers", "9", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]