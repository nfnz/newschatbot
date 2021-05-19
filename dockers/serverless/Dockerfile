FROM nikolaik/python-nodejs:python3.6-nodejs14

RUN apt-get update
RUN apt-get -y install gcc
RUN npm i -g serverless@2.x

ENTRYPOINT ["serverless"]