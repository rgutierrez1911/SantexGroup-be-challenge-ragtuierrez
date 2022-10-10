FROM  python:3.8.12-buster
WORKDIR /base_app
COPY . .
RUN pip install -r requirements_deque.txt
CMD python -m pub_sub