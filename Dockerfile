# Use a base Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variables
ENV GUNICORN_CONFIG=/app/gunicorn_config.py

# Expose the port
EXPOSE 8000

# Start the Gunicorn server
CMD ["gunicorn", "--config", "/app/gunicorn_config.py", "main:app"]