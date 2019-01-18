# This is your Editor pane. Write the Dockerfile here and 
# use the command line to execute commands
FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./server.py" ]