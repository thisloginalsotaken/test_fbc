FROM python:3.9.10

WORKDIR /app
COPY . .

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "/app/main.py"]
CMD []