
# Use the official uvicorn-gunicorn-fastapi image.
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

ENV PORT ${PORT}

ENV APP_HOME /app

ENV APP_MODULE example.main:app

ENV TIMEOUT 0

ENV LOG_LEVEL ${APOLLO_LOGGER_LEVEL}

ENV WORKERS ${WORKERS}

WORKDIR $APP_HOME

COPY ./requirements.txt ./

# Install production dependencies.
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy local code to the container image.
COPY . ./

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores vailable.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

CMD exec gunicorn --bind :$PORT --workers $WORKERS --worker-class uvicorn.workers.UvicornWorker --timeout $TIMEOUT $APP_MODULE  