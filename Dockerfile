FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8503
HEALTHCHECK CMD curl --fail http://localhost:8503/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8503", "--server.address=0.0.0.0"]