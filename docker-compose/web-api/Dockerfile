# This is the base image
FROM python:3.12

# This is the working directory (like running `cd /app`)
WORKDIR /app

# We are copying the requirements.txt file to the container
COPY web-api/requirements.txt .

# We are installing the dependencies
RUN pip install -r requirements.txt

# Copy the shared code
COPY shared/todo/ ./todo/

# Copy the application code
COPY web-api/main.py .

# Command to run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
