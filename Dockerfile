# PM Agent API for BusinessHub (Redmine integration).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    SNAPSHOT_DIRECTORY=/app/data/snapshots \
    DAILY_REPORT_DIRECTORY=/app/data/daily_reports \
    RUN_LOG_DIRECTORY=/app/data/logs

WORKDIR /app

# Keep dependency installation cached when only application code changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd --gid 10001 pmagent \
    && useradd --create-home --uid 10001 --gid pmagent pmagent \
    && mkdir -p /app/data/snapshots /app/data/daily_reports /app/data/logs \
    && chown -R pmagent:pmagent /app/data

COPY --chown=pmagent:pmagent app ./app
USER pmagent

EXPOSE 8090
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8090/health', timeout=5)" || exit 1

# One worker keeps the in-memory snapshot and AI caches consistent.
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8090", "--workers", "1"]
