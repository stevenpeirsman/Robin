FROM python:3.11-slim

WORKDIR /app

COPY Setup/Required_packages.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "Listening.py"]
