FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -e .
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
