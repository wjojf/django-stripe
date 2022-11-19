FROM python:3.11

RUN mkdir /site 
COPY . /site
WORKDIR /site

RUN pip install -r requirements.txt

WORKDIR /site/app


EXPOSE 8000
RUN python3 manage.py migrate

ENTRYPOINT [ "python3", "manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]