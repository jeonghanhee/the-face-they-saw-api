FROM python:3.14.3

WORKDIR /the-face-they-saw-api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["./start.sh"]