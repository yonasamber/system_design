FROM python:3.13-slim-bullseye

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install OS-level dependencies
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ffmpeg \
        default-libmysqlclient-dev \
        pkg-config \
        apt-transport-https \
        ca-certificates \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY . /app

# Default command
CMD ["python", "consumer.py"]