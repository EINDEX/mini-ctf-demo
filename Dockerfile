FROM python:3.10-alpine

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ARG token
RUN echo ${token} > /etc/token

COPY . .

EXPOSE 5000

CMD ["flask", "run", "-h","0.0.0.0"]