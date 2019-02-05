# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.6.1
COPY . /app
WORKDIR /app
ADD . /tmp
RUN sh -c "ls -ltr  /tmp"
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
