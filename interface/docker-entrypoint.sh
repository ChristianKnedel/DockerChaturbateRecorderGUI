#!/bin/bash


echo "-> lösche Cache"
find . | grep -E "(migrations|__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

echo "-> Migrate"
python3 manage.py makemigrations main
python3 manage.py migrate

echo "-> compilemessages"
#python3 manage.py compilemessages

echo "-> starte server "
python3 manage.py runserver 0.0.0.0:8000
