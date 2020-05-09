FROM python:3.8
WORKDIR '.'
#RUN apt-get update || : && apt-get install python3 -y
RUN sudo add-apt-repository universe
RUN sudo apt-get install python3
RUN sudo apt-get install python3-pip
RUN python --version
RUN pip3 freeze > requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir


FROM node:14.2.0

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

#CMD [ "npm", "run", "dev" ]
CMD [ "node", "--max-old-space-size=4096", "main.js" ]