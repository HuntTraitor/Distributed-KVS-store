FROM python:3.12
RUN apt-get -y update

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8090

WORKDIR /app

COPY ./requirements.txt /app

RUN python -m pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]