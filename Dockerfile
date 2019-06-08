# Download base image
FROM python:3.6
WORKDIR /app

# Download packages to container file system
COPY requirements.txt /app
RUN pip install -r ./requirements.txt

# Run app in container
COPY app.py /app
CMD ["python", "app.py"]
