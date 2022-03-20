FROM python:latest
WORKDIR shorturl
COPY requirements.txt /shorturl/
RUN  pip install -r requirements.txt
COPY . /shorturl/
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "makemigrations", "shorturl"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "init"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8090"]