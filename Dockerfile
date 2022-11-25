FROM node:18.12.1-buster as bulder

WORKDIR /app

COPY web/package.json web/yarn.lock ./

RUN yarn install

COPY web/ ./

RUN yarn build

FROM python:3.10.8-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY analyse analyse
COPY catboost_model catboost_model

COPY flask flask
COPY --from=bulder /app/dist /flask/static

EXPOSE 5000

CMD [ "cd flask && python", "flask/hello.py" ]