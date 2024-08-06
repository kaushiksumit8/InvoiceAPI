# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variable for non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install the necessary Python packages
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]
