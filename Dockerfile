FROM python:3.9.7-slim-buster

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/
COPY . .

CMD [ "python", "./main.py" ]
