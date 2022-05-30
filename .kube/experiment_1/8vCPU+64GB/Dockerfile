FROM python:3.8

WORKDIR /app

# install dependencies
COPY ./.kube/experiment_1/8vCPU+64GB/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy fastAPI app codebase
COPY ./api /app

# run the fastAPI app
CMD ["gunicorn", "main:app", "--workers", "17", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]