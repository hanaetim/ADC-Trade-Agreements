FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
COPY app/ ./app/
ARG INSTALL_SPEC=.
RUN pip install --no-cache-dir "$INSTALL_SPEC"

# Copy additional application files
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Copy entrypoint script
COPY docker-entrypoint.sh ./
RUN chmod +x ./docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint and command
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
