# Use an official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app


COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port (5000)
EXPOSE 8080

# Run Flask directly (without Gunicorn)
CMD ["python3", "app.py"]
