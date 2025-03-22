
FROM python:3.9


WORKDIR /Users/tomasnagy/FastAPI/application


COPY ./requirements.txt /Users/tomasnagy/FastAPI/application/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /Users/tomasnagy/FastAPI/application/requirements.txt


COPY . /Users/tomasnagy/FastAPI/application/


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


# CMD ["fastapi", "run", "app/main.py", "--port", "80"]docker info

