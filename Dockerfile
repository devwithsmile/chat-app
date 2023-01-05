FROM python:3


WORKDIR /
    
COPY requirements.txt ./
    


RUN apt update -y
RUN apt install build-essential libdbus-glib-1-dev libgirepository1.0-dev -y
RUN apt-get install python-dev -y
RUN apt-get install libcups2-dev -y
RUN apt install libgirepository1.0-dev -y


RUN pip install pycups
RUN pip install cmake
RUN pip install dbus-python
RUN pip install reportlab
RUN pip install PyGObject 

RUN pip install -r requirements.txt

    
COPY . .

CMD ["python3","main.py"]