# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables for Python and Docker
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies including graphviz (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /code/

# Expose the port on which Django runs (default is 8000)
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver"]