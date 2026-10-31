# Use Python 3.11 slim image for efficiency
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8081 for incoming connections
EXPOSE 8081

# Run the SSE server
# Inside the container the server must listen on all interfaces; publish the port on
# 127.0.0.1 only (docker run -p 127.0.0.1:8081:8081 ...).
CMD ["python", "terminal_server_sse.py", "--host", "0.0.0.0"]