FROM python:3.10-slim
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY ./src /fastapi/app/src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]