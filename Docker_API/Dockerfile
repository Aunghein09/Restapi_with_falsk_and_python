FROM python:3.10
# flask run at port 5000
EXPOSE 5000 
# move to /app dir in the container 
WORKDIR /app
RUN pip install flask
# copy everything in the current dir to current dir of container
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]