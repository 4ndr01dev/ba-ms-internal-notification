# Use Python slim image as base
FROM python:3.13-slim-bookworm

# Set environment variables
# Explanation:
# - PYTHONUNBUFFERED: Ensure that Python output is not buffered (useful for logging).
# - PYTHONDONTWRITEBYTECODE: Disable the creation of .pyc files (bytecode).
# - PIP_NO_CACHE_DIR: Disable caching of pip packages.
# - PIP_DISABLE_PIP_VERSION_CHECK: Disable checking for pip version.
# - UV_SYSTEM_PYTHON: Use the system Python.
# - UV_PROJECT_ENVIRONMENT: Set the project environment to /usr/local.
# - PYTHONPATH: Set the Python path to the app directory.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    PYTHONPATH=/app

# Install system dependencies
# Explanation:
# - curl: For downloading packages.
# - gcc, g++: For building some Python packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    # curl \
    # gcc \
    g++ \
    # Remove apt lists to reduce image size.
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip
RUN pip install --no-cache-dir --root-user-action=ignore uv

# Set work directory
WORKDIR /app

# Copy dependency files
# pyproject.toml and uv.lock are copied first to leverage Docker layer caching
# We install dependencies directly into the system Python to keep the image lean
# and avoid the overhead of a virtual environment in the container
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# Explanation:
# - --no-dev: Don't install development dependencies.
# - --no-cache: Don't use the package cache (reduces image size).
# - --compile-bytecode: Compile bytecode for faster startup.
RUN uv sync --no-dev --no-cache --compile-bytecode

# Copy source code
COPY src/ ./src/

# Create non-root user for security
# Explanation:
# - useradd: Create a new user called app.
# - create-home: Create a home directory for the user.
# - shell /bin/bash: Set the shell for the user to bash.
# - chown -R app:app /app: Change the ownership of the /app directory to the app user.
# - USER app: Set the user to app.
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Set the default command
ENTRYPOINT ["python", "-m", "src"]

# CMD ["--help"]
