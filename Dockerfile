FROM python:3.8-slim
WORKDIR /src
RUN pip install pyyaml Flask
COPY ./src /src
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

