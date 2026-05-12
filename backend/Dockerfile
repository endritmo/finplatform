# ── Stage: production backend ──────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Install OS-level dependencies (gcc needed for some pip packages)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached as a separate layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . .

# Copy and enable the entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh   # ← strip Windows CR characters
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]


