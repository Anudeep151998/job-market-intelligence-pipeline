# 1. Use a lightweight Python 3.11 image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies for reliability
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire project into the container
COPY . .

# 6. Streamlit runs on port 8501 by default
EXPOSE 8501

# 7. Start the Dashboard when the container launches
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]