# Menggunakan base image Python Alpine
FROM python:3.9-slim

# 1. Install dependensi sistem untuk firebird
RUN apt-get update && apt-get install -y \
        libfbclient2\
        && rm -rf /var/lib/apt/lists/*

# 2. Set direktori kerja
WORKDIR /app

# Copy dan install requirements.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port Flask
EXPOSE 5000

# 5. Jalankan aplikasi
CMD ["python", "piutang.py"]