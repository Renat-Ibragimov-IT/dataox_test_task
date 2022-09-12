FROM python:3.9
WORKDIR /dataox_test_task
COPY . ./dataox_test_task
COPY requirements.txt /dataox_test_task/

RUN python -m venv /opt/venv
RUN pip install --upgrade pip
RUN pip install --requirement /dataox_test_task/requirements.txt