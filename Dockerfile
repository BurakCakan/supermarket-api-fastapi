FROM python:3.8

COPY requirements.txt requirements.txt 

RUN pip3 install -r requirements.txt

WORKDIR /app

COPY . /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]