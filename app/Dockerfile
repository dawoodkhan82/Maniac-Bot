FROM node:14.2.0
RUN apt-get update || : && apt-get install python3 -y

WORKDIR /app
COPY . /app

#ENV PATH /usr/bin:$PATH
RUN npm install
RUN python3 --version
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 freeze > requirements.txt
RUN pip3 list

#COPY package*.json/
RUN ls
CMD [ "node", "--max-old-space-size=4096", "main.js" ]
