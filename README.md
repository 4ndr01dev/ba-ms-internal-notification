![Logo](https://storage.googleapis.com/basic-resources/bloom%20logo%20color.svg)

# Internal Notification Service

Scheduled alert evaluation system that monitors time-series data across multiple fronts and sends Slack notifications based on spike, threshold, and no-data conditions.

## Architecture

Cloud Scheduler → Cloud Run Job → (InfluxDB + BigQuery) → Alert Evaluation → Slack + Firestore

## Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) package manager
- `gcloud` CLI authenticated with Application Default Credentials (ADC) for local development:
  ```bash
  gcloud auth application-default login
  ```

## Local Setup

```bash
# Clone and navigate to the project
cd ba-ms-internal-notification

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
uv sync

# Copy environment configuration
cp .env.example .env
# Edit .env and fill in required values (see .env.example for details)
```

### Development Setup

```bash
# Install with development dependencies
uv sync --all-groups

# Install pre-commit hooks
pre-commit install

# Run code quality checks
pre-commit run --all-files
```

## Run Locally

```bash
# Basic usage with operational time series
uv run python -m src --ts-id "example-ts-001" --type operational

# Using satelite time series
uv run python -m src --ts-id "sat-ts-042" --type satelite

# Enable debug logging
uv run python -m src --ts-id "example-ts-001" --type operational --max-level-logging "DEBUG"
```

## Configuration

- **Local environment**: Copy [.env.example](.env.example) to `.env` and configure all required variables
- **Production secrets**: Managed via GCP Secret Manager (never committed to the repository)
- **Configuration reference**: See [src/configs/params.py](src/configs/params.py) for parameter definitions

## Deployment

The service runs as a **Cloud Run Job** triggered by **Cloud Scheduler**:

1. Cloud Scheduler creates a job execution for each front on a fixed schedule
2. Cloud Run Job reads configuration from Secret Manager
3. Job evaluates alert conditions and sends notifications
4. State is persisted to Firestore for deduplication

Deployment is managed via container builds and Cloud Run Job updates. Each front is configured as a separate scheduled trigger.

## Project Structure

```
.
├── src/
│   ├── __main__.py              # CLI entrypoint
│   ├── configs/                 # Configuration and parameter definitions
│   │   ├── params.py            # Application parameters
│   │   ├── paths.py             # Path configurations
│   │   └── types.py             # Type definitions
│   ├── conn/                    # External service connections
│   │   ├── service_conn.py      # Service authentication
│   │   └── token_store_redis.py # Redis token cache
│   ├── etl/                     # Data processing pipeline
│   │   ├── extract.py           # Data extraction (InfluxDB/BigQuery)
│   │   ├── transform.py         # Alert evaluation logic
│   │   └── load.py              # Notification sending (Slack/Firestore)
│   ├── schemas/                 # Data models and validation
│   └── utils/                   # Logging, secrets, utilities
├── workflows/                   # Cloud Scheduler/Workflow definitions
│   └── workflows.yaml.example   # Example workflow configuration
├── Dockerfile                   # Container image definition
├── pyproject.toml              # Project dependencies and configuration
└── uv.lock                     # Dependency lock file
```

## Troubleshooting

- **Authentication errors**: Ensure `gcloud auth application-default login` is configured for local development
- **Missing environment variables**: Verify all required variables in `.env` match [.env.example](.env.example)
- **Permission denied**: Check IAM roles for Firestore, BigQuery, and Secret Manager access in your GCP project
