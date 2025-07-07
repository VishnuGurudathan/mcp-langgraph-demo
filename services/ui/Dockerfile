FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./src ./src

# Copy .streamlit config
COPY .streamlit /app/.streamlit

CMD ["streamlit", "run", "src/chat_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
