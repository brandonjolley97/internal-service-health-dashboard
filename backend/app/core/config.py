import os

# Reading environment variable if present, or using a default if not.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/health_dashboard"
)