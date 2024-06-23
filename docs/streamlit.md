# Report of Streamlit Service

On this this stage was written frontend part of ml service using Streamlit framework [tone_app.py](../mlops_course/streamlit/tone_app.py).
This designed to predict tonality of input text, which user send to dialog window.

# Backend of app

The backend is implemented as a separate REST API service by python web-framework FastApi. A pre-trained transformer model is used as a model

[Repository of service](https://gitlab.com/ivan_golt/text_tone_service)

This service can be started in two ways:

1) Using docker-compose: `docker-compose up --build` 
2) Running locally on machine: `poetry run uvicorn src.app:app --host localhost --port 8000`

# Running Streamlit

Streamlit run with one command: `streamlit run ../mlops_course/streamlit/tone_app.py`


# Example of work 
![](../docs/streamlit%20service.png)