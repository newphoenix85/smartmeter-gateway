FROM python:3.12


ADD app /srv/app
ADD main.py /srv/
ADD requirements.txt /srv/

WORKDIR /srv

RUN pip install --no-cache-dir -r /srv/requirements.txt
ENV PYTHONPATH=/srv

CMD [ "sh", "-c", "python /srv/app/main.py" ]

