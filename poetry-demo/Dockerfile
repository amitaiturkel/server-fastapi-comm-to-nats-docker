# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy your FastAPI server code into the container
COPY . .

# Expose the port your FastAPI server will run on
EXPOSE 8000

# Define the command to run your FastAPI server
CMD ["uvicorn", "poetry_demo.fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
