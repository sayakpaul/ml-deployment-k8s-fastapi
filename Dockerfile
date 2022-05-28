FROM python:3.8

WORKDIR /app

# install dependencies
COPY ./api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy fastAPI app codebase
COPY ./api /app

# run the fastAPI app
CMD ["uvicorn", "main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "80"]