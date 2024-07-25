FROM python:3.11

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Set working directory
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt


# Create necessary directories
RUN mkdir -p /staticfiles /media /nonexistent

# Expose port
EXPOSE 8000


# Command to run the application
CMD ["uvicorn", "busstation.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
