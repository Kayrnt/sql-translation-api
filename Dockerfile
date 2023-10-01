# Use an official Python runtime as a parent image
FROM python:3.11.5-slim-bullseye

# update system and add git
RUN apt-get update && apt-get install -y git

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

# Create and set the working directory
WORKDIR /app

# Copy the pyproject.toml file to the container
COPY pyproject.toml ./

# Install poetry and dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Install Gunicorn
RUN pip install gunicorn    

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 80
EXPOSE 80

# Use Gunicorn as the production WSGI server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]