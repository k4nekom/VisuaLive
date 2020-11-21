FROM python:3.7

WORKDIR /app

COPY app/requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app/ ./

# CMD python run.py