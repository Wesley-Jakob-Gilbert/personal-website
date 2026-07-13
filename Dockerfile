# ── Stage 1: Build static files with Python ───────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install Python deps first (cached layer — only invalidated when requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source and run the build script
COPY . .
RUN python build.py

# ── Stage 2: Serve with Nginx ─────────────────────────────────────────────
# Multi-stage build: the final image contains only Nginx + the dist/ files.
# No Python, no source code, no build tools — keeps the image small (~25 MB).
FROM nginx:1.27-alpine AS server

COPY --from=builder /app/dist    /usr/share/nginx/html
COPY nginx.conf                  /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -qO- http://localhost/ || exit 1
