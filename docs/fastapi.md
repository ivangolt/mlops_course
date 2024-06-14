# Deploying a machine learning model

On this stage was create an application to analyze text tone using FastAPI, Celery, RabbitMQ and Redis.

The application provides an asynchronous, highly loaded API to interact with a machine learning model. The example uses a pre-trained Transformer model to predict sentiment for input text.

# Repository of project 

This project consits in separate repository [repository](https://gitlab.com/ivan_golt/ml_service_fastapi_celery_rabbitmq_redis).

# Structure of project

```
.
├── .docker
│   └── Dockerfile              # Docker image with app
├── docker-compose.yml          # Docker container managing
├── pyproject.toml              # Dependencies
└── src
    ├── app.py                  # Main app, FastAPI initializing
    ├── api                     # Package with API routes
    │   ├── __init__.py
    │   └── routes              # Package with API routes
    │       ├── __init__.py
    │       ├── healthcheck.py  # Route to check the srvice status
    │       ├── predict.py      # Route for model predictions
    │       └── router.py       # Main router
    ├── celery                  # Package with data models
    │   ├── __init__.py
    │   ├── celery_init.py      # Celery initializing
    │   └── worker.py           # Celery worker
    └── services                # Package with ML model
        ├── __init__.py
        ├── model.py            # ML model with prediction
        └── utils.py            # Supporting utilities

```

# Program description

- The client sends an HTTP request with text data in json to the FastAPI asynchronous endpoint.
- FastAPI receives the request, validates it, and creates a new Celery task.
- Celery asynchronously places the task in the queue of the RabbitMQ broker running "under the hood".
- The Celery Worker asynchronously retrieves the task from the RabbitMQ queue, then sends a query to the ML model, receives a response, and returns the result.
- Redis is used to cache intermediate results and speed up repeated queries with the same data.
- The response is returned via RabbitMQ to FastAPI, which sends it back to the client as an HTTP response.

# Application startup

`docker-compose up --build`


# Work logs

```
rabbitmq-1       | 2024-06-12 20:09:56.386314+00:00 [info] <0.1038.0> accepting AMQP connection <0.1038.0> (172.19.0.5:37890 -> 172.19.0.3:5672)
rabbitmq-1       | 2024-06-12 20:09:56.401651+00:00 [info] <0.1038.0> connection <0.1038.0> (172.19.0.5:37890 -> 172.19.0.3:5672): user 'guest' authenticated and granted access to vhost '/'
celery-worker-1  | 2024-06-12 20:09:56.483 | INFO     | src.celery.worker:predict_tonality:16 - Start prediction task: 7e258a52-6b8e-4ec3-83c3-be8d8f6b75a2
celery-worker-1  | 2024-06-12 20:09:58.764 | INFO     | src.celery.worker:predict_tonality:20 - Input text: string
celery-worker-1  | 2024-06-12 20:09:58.765 | INFO     | src.celery.worker:predict_tonality:21 - Predicted: {'label': 'neutral', 'score': 0.9558939337730408}
celery-worker-1  | 2024-06-12 20:09:58.765 | INFO     | src.celery.worker:predict_tonality:22 - Completing prediction task 7e258a52-6b8e-4ec3-83c3-be8d8f6b75a2
mlapp-1          | INFO:     172.19.0.1:49400 - "POST /api/predict/ HTTP/1.1" 200 OK
mlapp-1          | INFO:     172.19.0.1:36742 - "GET /openapi.json HTTP/1.1" 200 OK
```