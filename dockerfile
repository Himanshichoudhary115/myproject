# Use a base image with Python
FROM python:3.9-slim

# Install system dependencies for OpenCV, libGL, etc.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy project files to container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "Home.py"]

