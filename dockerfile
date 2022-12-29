FROM python:3

ADD . /app
    
COPY requirements.txt ./
    
WORKDIR /app
RUN pip install PyGObject
RUN pip install -r requirements.txt

    
COPY . .
    

CMD ["python3","main.py"]
