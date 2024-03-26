FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ~/Raffle

COPY . ./app

RUN apt-get update && apt-get install libgl1 zbar-tools -y
RUN pip install --no-cache-dir -r ./app/requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

CMD ["python", "-m", "app"]