#!/bin/sh
ADDRESS=${1:-127.0.0.1:8000}
gunicorn main:app -b $ADDRESS --log-file -
