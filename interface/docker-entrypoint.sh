#!/bin/bash

usermod -u $UID recorder
groupmod -g $GID recorder

echo "-> lösche Cache"
find . | grep -E "(migrations|__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

echo "-> Migrate"
python3 manage.py makemigrations main
python3 manage.py migrate

echo "-> compilemessages"
#python3 manage.py compilemessages

echo "-> starte server "
chown -R recorder:recorder /code/
su recorder -c "python3 manage.py runserver 0.0.0.0:8000"
