#using python 3.11 and the requirements.txt it should work
FROM python:3.11-slim 

WORKDIR /app

COPY requirements.txt .
#copy requirements to all destinations
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# copy all project files to all 
ENV PYTHONUNBUFFERED=1
#env pythonunbuffer=1 sends python print output directly to output to avoid dockerlogs being delayed or empty
CMD ["python","run.py"]