#! /bin/bash

MYSQL_USER=root \
  MYSQL_PASSWORD=password \
  MYSQL_HOST=127.0.0.1 \
  MYSQL_PORT=3306 \
  FLASK_APP=web.py \
  python web.py
