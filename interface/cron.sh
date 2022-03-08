#!/bin/bash
for variable_value in $(cat /proc/1/environ | sed 's/\x00/\n/g'); do
   export $variable_value
done


for n in {1..5}
do
   #uptime
   cd /code/ && /usr/bin/python3 manage.py check_chatrubate &
   sleep 9
done
