FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY math_tool.py .
ENTRYPOINT ["python", "math_tool.py"]
