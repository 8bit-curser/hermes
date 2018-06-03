FROM python:3.6.3
LABEL mantainer "Tomas Vukasovic <tvukasovic@outlook.com>"
RUN apt-get update
ADD . hermes/ 
WORKDIR /hermes
RUN pip install -r requirements.txt
CMD ["python", "hermes/app/app.py"]
