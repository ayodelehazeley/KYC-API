FROM python:3.10-slim

RUN apt-get update && apt-get install -y tesseract-ocr

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn","kyc_api:app","--host","0.0.0.0","--port","8000"]
