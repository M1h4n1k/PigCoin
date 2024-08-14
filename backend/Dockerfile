FROM python:3.12-slim
WORKDIR /backend
COPY ./requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
COPY . .
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--forwarded-allow-ips", "*"]
