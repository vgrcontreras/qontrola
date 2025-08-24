FROM python:3.12-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script first and make it executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Copy the rest of the application
COPY . .

# Expose the port the app will run on
EXPOSE 8000