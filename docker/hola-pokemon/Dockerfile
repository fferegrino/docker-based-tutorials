# This is the base image
FROM python:3.12

# This is the working directory (like running `cd /app`)
WORKDIR /app

# We are copying the requirements.txt file to the container
COPY requirements.txt .

# We are installing the dependencies
RUN pip install -r requirements.txt

# We are copying the app.py file to the container
COPY app.py .

# This is the command to run when the container starts
CMD ["python", "app.py"]
