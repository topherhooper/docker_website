FROM python:2-onbuild
RUN pip install Flask
ADD . /code
WORKDIR /code
CMD python app.py