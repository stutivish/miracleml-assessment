FROM postgres:latest

ENV POSTGRES_USER=testuser \
    POSTGRES_PASSWORD=testpassword \
    POSTGRES_DB=clinical_trials

# Copy the initialization SQL script into the Docker container
COPY init_db.sql /docker-entrypoint-initdb.d/