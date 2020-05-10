FROM python:3.8

WORKDIR '.'

COPY . .

ENV PATH /usr/bin:$PATH

RUN apt-get install python3
RUN python3 --version
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 freeze > requirements.txt
RUN pip3 list

FROM node:14.2.0

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production
COPY . .

CMD [ "node", "--max-old-space-size=4096", "main.js" ]
