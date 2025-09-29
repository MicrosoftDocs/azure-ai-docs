# Minimal development Dockerfile for Stage 1 prototype
# [TO VERIFY] Use official Azure AI Foundry base image if guidance exists.
FROM mcr.microsoft.com/devcontainers/python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY assets ./assets
ENV PYTHONPATH=/app/src

# Default command runs batch evaluation harness (adjust as desired)
CMD ["python", "-m", "agent_app.run_batch_eval"]
