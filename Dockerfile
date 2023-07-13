FROM python:latest
WORKDIR /Car_service_CRM
COPY /requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt
COPY . /Car_service_CRM