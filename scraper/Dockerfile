# Dockerfile for web scraper
FROM python3.10

# Install dependencies
RUN pip install -r requirements.txt

# Set working directory
WORKDIR /app

COPY . .

CMD ["python3" "scraper.py"]