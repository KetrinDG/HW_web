FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /data

COPY . .

EXPOSE 3000
EXPOSE 5000/udp

CMD ["python", "main.py"]
