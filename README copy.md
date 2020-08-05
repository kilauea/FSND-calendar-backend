# FSND-capstone
Final Full Stack Nano Degree project

## On MacOS if you installed postgres using Homebrew

```sh
brew services start postgresql
brew services stop postgresql
```

## DB migration

```sh
dropdb calendarapp && createdb calendarapp
rm -rf migrations
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

curl http://localhost:5000/api/calendars/ -H "content-type: application/json" -X GET

curl http://localhost:5000/api/calendars/1/ -H "content-type: application/json" -X GET

curl http://localhost:5000/api/calendars/ -H "content-type: application/json" -d '{"name": "qwqeqweqweqw", "description": "qewfeqfqf", "min_year": 1900, "max_year": 2200, "time_zone": "Europe/Madrid", "week_starting_day": 0, "emojis_enabled": true, "show_view_past_btn": true}'

curl http://localhost:5000/api/calendars/6/ -H "content-type: application/json" -X DELETE

curl http://localhost:5000/api/calendars/4/ -H "content-type: application/json" -d '{"name": "Calendar 4"}' -X PATCH

curl http://localhost:5000/api/calendars/1/tasks/ -H "content-type: application/json" -d '{"title": "Test Task", "color": "#2966B8", "details": "Testing curl", "start_time": "2020-08-01, 00:00:00", "end_time": "2020-08-01, 23:59:59", "is_all_day": true, "is_recurrent": false, "repetition_value": 0, "repetition_type": "", "repetition_subtype": ""}'

curl http://localhost:5000/api/calendars/1/tasks/1/ -H "content-type: application/json" -X GET