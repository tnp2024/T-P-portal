# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Command to run the Django development server
CMD ["gunicorn", "finalproj2.wsgi:application", "--bind", "0.0.0.0:8000"]
