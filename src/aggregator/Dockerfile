# Use an official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy and install requirements
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

# Copy files to the container
COPY save_artist.py .
COPY server_vars.py .
COPY resources/artists/artist-1.json ./resources/artists/artist-1.json

# Command to run application
CMD ["python", "save_artist.py"]