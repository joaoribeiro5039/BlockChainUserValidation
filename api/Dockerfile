FROM python:3.11-slim

RUN mkdir /api

WORKDIR /usr/src/api

COPY api.py .

RUN pip install --upgrade pip
# RUN pip install hashlib
RUN pip install redis
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install pydantic

EXPOSE 6379
EXPOSE 8000

CMD ["python","api.py"]