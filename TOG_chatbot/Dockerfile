FROM python:3.10-slim

WORKDIR /WORKDIR


# Install PostgreSQL client libraries and other system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY ./pyproject.toml /WORKDIR/
COPY ./app /WORKDIR/app
COPY ./src /WORKDIR/src
COPY ./.env /WORKDIR/.env


# Upgrade pip to the latest version
RUN pip install -e .


CMD ["fastapi", "run", "app/main.py","--host","0.0.0.0", "--port", "80"]