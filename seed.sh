#!/bin/bash

rm -rf Eventplannerapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations Eventplannerapi
python3 manage.py migrate Eventplannerapi
python3 manage.py loaddata users
python3 manage.py loaddata event_users
python3 manage.py loaddata categories
python3 manage.py loaddata food_types
python3 manage.py loaddata food_tables
python3 manage.py loaddata events
python3 manage.py loaddata food_planners

# Create a seed.sh file in your project directory
# Place the code below in the file.
# Run chmod +x seed.sh in the terminal.
# Then run ./seed.sh in the terminal to run the commands.
