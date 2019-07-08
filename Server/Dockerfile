FROM node:carbon

LABEL maintainer Ilija Vukotic <ivukotic@cern.ch>

# Create app directory
WORKDIR /usr/src/app

COPY . .
RUN npm install

EXPOSE 80

CMD [ "npm","start" ]