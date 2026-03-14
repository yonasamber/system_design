FROM python:3.13-slim-bullseye

# Install OS-level dependencies needed to build mysqlclient and other packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY . /app

# Expose port
EXPOSE 8080

# Default command
CMD ["python", "server.py"]