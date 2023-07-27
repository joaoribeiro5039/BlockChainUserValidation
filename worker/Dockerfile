FROM python:3.11-slim

RUN mkdir /worker

WORKDIR /usr/src/worker

COPY worker.py .

RUN pip install --upgrade pip
RUN pip install redis
RUN pip install pydantic

EXPOSE 6379

CMD ["python","worker.py"]