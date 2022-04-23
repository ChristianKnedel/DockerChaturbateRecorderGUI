#!/bin/bash
for variable_value in $(cat /proc/1/environ | sed 's/\x00/\n/g'); do
   export $variable_value
done



for n in {1..5}
do
   #uptime

    if [ "$COMMAND_ADAPTER" != "DockerAdapter" ]
    then
        su -l -p recorder -c "cd /code/ && /usr/bin/python3 manage.py check_chatrubate" &
    else
        cd /code/ && /usr/bin/python3 manage.py check_chatrubate &
    fi

   
   sleep 9
done
