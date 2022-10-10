FROM  python:3.8-buster
WORKDIR /base_app
COPY . .
RUN pip install -r requirements.txt
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-config log_conf.yml
#CMD gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker