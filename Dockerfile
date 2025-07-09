# Backend stage
FROM python:3.11-slim AS backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# Frontend stage
FROM node:18 AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Final stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /app/frontend/dist /app/frontend/dist
RUN pip install gunicorn
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
