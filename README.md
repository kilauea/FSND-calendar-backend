FSND-calendar-backend
---------------------

## Introduction

Backend application for the Capstone project, Udacity Full Stack Nano Degree

FSND-calendar-backend is an application that allows to create calendars and create tasks in each calendar.

## Local development

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by using the `requirements.txt` file running:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file into the virtual environment.

### Running the application

To run the application execute the following command, using the provided run.py file:

```bash
source venv/bin/activate
python run.py
```

### Unittesting

The file test_calendar.py contains backend application unit tests.

To run the unit tests run the following command:

```bash
source venv/bin/activate
python test_calendar.py
```

## Heroku deplyoment

The backend application can be deployed to Heroku following the next steps.

### Install Heroku and login

```bash
brew tap heroku/brew && brew install heroku
heroku login
```

### Create Heroku app

To create the application, calendar-backend-acv, run the following command:

```bash
% heroku create calendar-backend-acv
Creating ⬢ calendar-backend-acv... done
https://calendar-backend-acv.herokuapp.com/ | https://git.heroku.com/calendar-backend-acv.git
```
### Add git remote for Heroku to local repository

Now we need to add a git remote to the Heroku Git:

```bash
% git remote add heroku https://git.heroku.com/calendar-backend-acv.git
```

### Add postgresql add on for our database

The last step is to create a postgresql database for the application:

```bash
% heroku addons:create heroku-postgresql:hobby-dev --app calendar-backend-acv
Creating heroku-postgresql:hobby-dev on ⬢ calendar-backend-acv... free
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
```

```bash
heroku config --app calendar-backend-acv
=== calendar-backend-acv Config Vars
DATABASE_URL: postgres://fvlgncowlnwdci:8db3311b2d1363b4a62c0729673aca8f72d33cb685a099b21795b0ad15c6d947@ec2-54-243-67-199.compute-1.amazonaws.com:5432/dadeus8j8nhtin
```

The database URL will be available in Hekoku through the enviroment variable DATABASE_URL that will be used by the application.

### Setup required environment

* Open the settings in the Heroku app website.
* Reveal Config Vars.
* Add the FLASK_ENV variable.

![Config Vars](images/Heroku_Config_Vars_backend.png?raw=true)

### Push the application

To actually deploy the application we have to push it into the Heroku Git. We can use the script herokuDeployment.sh

```bash
% ./herokuDeployment.sh
```

### Run migrations

Now we need to run the migrations to initialize the database

```bash
% heroku run python manage.py db upgrade --app calendar-backend-acv
Running python manage.py db upgrade on ⬢ calendar-backend-acv... up, run.3502 (Free)
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 437ef732aa0e, Initial migration.
INFO  [alembic.runtime.migration] Running upgrade 437ef732aa0e -> 91aac5980055, Remove User model
```

### Test the deplaoyed application

We can run the following curl command to test if the application is running.

```bash
% curl https://calendar-backend-acv.herokuapp.com/api/calendars/ -H "content-type: application/json" -X GET
```

We should get the following json:

```json
{
  "calendars": [
    {
      "id": 1,
      "date_created": "2020-08-05, 20:26:33",
      "date_modified": "2020-08-05, 20:26:33",
      "name": "Main floor calendar",
      "description": "Main floor emplyees calendar",
      "min_year": 2000,
      "max_year": 2200,
      "time_zone": "Europe/Madrid",
      "week_starting_day": 0,
      "emojis_enabled": true,
      "show_view_past_btn": true,
      "auto_decorate_task_details_hyperlink": true,
      "hide_past_tasks": false,
      "days_past_to_keep_hidden_tasks": 62
    }
  ],
  "n_calendars": 1,
  "success": true
}
```

## API Documentation

### GET /calendars/
- General:
  - Returns a dictionary with all the abailable calendars in a list, the number of existing calendars and success value
- Sample: `curl http://127.0.0.1:5000/api/calendars/ | jq .`
  - On success:
```json
{
  "calendars": [
    {
      "auto_decorate_task_details_hyperlink": true,
      "date_created": "2020-08-03, 19:21:27",
      "date_modified": "2020-08-04, 18:45:07",
      "days_past_to_keep_hidden_tasks": 62,
      "description": "awcwec24fq24fq2f 234 f",
      "emojis_enabled": true,
      "hide_past_tasks": false,
      "id": 7,
      "max_year": 2200,
      "min_year": 1900,
      "name": "2nd floor calendar",
      "show_view_past_btn": true,
      "time_zone": "Europe/Madrid",
      "week_starting_day": 0
    },
    {
      "auto_decorate_task_details_hyperlink": true,
      "date_created": "2020-07-23, 23:55:40",
      "date_modified": "2020-08-05, 19:26:19",
      "days_past_to_keep_hidden_tasks": 62,
      "description": "Main floor emplyees calendar",
      "emojis_enabled": true,
      "hide_past_tasks": true,
      "id": 1,
      "max_year": 2200,
      "min_year": 2000,
      "name": "Main floor calendar",
      "show_view_past_btn": true,
      "time_zone": "Europe/Madrid",
      "week_starting_day": 0
    }
  ],
  "n_calendars": 2,
  "success": true
}
```
  - On error return the following dictionary:
```json
{
  "success": false,
  "n_calendars": 0
}
```

### POST /calendars/
- General:
  - Creates a new calendar
  - Returns a dictionary with success true and calendar_id if caleras was created
- Sample: `curl http://127.0.0.1:5000/api/calendars/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" -d '{"name": "New calendar", "description": "This is a new calendar", "min_year": 1900, "max_year": 2200, "time_zone": "Europe/Madrid", "week_starting_day": 0, "emojis_enabled": true, "show_view_past_btn": true}' | jq .`
  - On success
```json
{
  "calendar_id": 11,
  "success": true
}
```
  - On error:
```json
{
  "success": false
}
```

### GET /calendars/<int:calendar_id>/
- General:
  - Get a calendar by its id
  - Returns a dictionary with the requested calendar
- Sample: `curl http://127.0.0.1:5000/api/calendars/11/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" | jq .`
  - On success
```json
{
  "calendar": {
    "auto_decorate_task_details_hyperlink": true,
    "date_created": "2020-08-06, 21:59:20",
    "date_modified": "2020-08-06, 21:59:20",
    "days_past_to_keep_hidden_tasks": 62,
    "description": "This is a new calendar",
    "emojis_enabled": true,
    "hide_past_tasks": false,
    "id": 11,
    "max_year": 2200,
    "min_year": 1900,
    "name": "New calendar",
    "show_view_past_btn": true,
    "time_zone": "Europe/Madrid",
    "week_starting_day": 0
  },
  "success": true
}
```

### DELETE /calendars/<int:calendar_id>/
- General:
  - Deletes a calendar by its id
  - Returns a dictionary with success true, the deleted calendar name and the calendar id if the calendar was deleted
- Sample: `curl http://127.0.0.1:5000/api/calendars/11/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" -X DELETE | jq .`
```json
  - On success
  {
  "calendar_id": 11,
  "name": "New calendar",
  "success": true
}
```

### PATCH /calendars/<int:calendar_id>/
- General:
  - Modifies a calendar by its id
  - Returns a dictionary with success true, the modified calendar name and the calendar id if the calendar was modified
- Sample: `curl http://127.0.0.1:5000/api/calendars/7/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" -d '{"week_starting_day": 6}' -X PATCH| jq .`
- On success
```json
{
  "calendar_id": 7,
  "name": "2nd floor calendar",
  "success": true
}
```

### GET /calendars/<int:calendar_id>/tasks/?y=<int:year>&m=<int:month>&page=<int:page_number>
- General:
  - Gets the tasks of the calendar indicated by its id, at the indicated year and month. If no year and month are given the current date is used. The returned tasks are paginated, with a maximun of 10 tasks per page.
  - Returns a dictionary with the calendar information, the tasks, the number of tasks, the year, month and success true
- Sample: `curl http://127.0.0.1:5000/api/calendars/1/tasks/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" | jq .`
- On success
```json
{
  "calendar": {
    "auto_decorate_task_details_hyperlink": true,
    "date_created": "2020-07-23, 23:55:40",
    "date_modified": "2020-08-05, 19:26:19",
    "days_past_to_keep_hidden_tasks": 62,
    "description": "Main floor emplyees calendar",
    "emojis_enabled": true,
    "hide_past_tasks": true,
    "id": 1,
    "max_year": 2200,
    "min_year": 2000,
    "name": "Main floor calendar",
    "show_view_past_btn": true,
    "time_zone": "Europe/Madrid",
    "week_starting_day": 0
  },
  "month": 8,
  "n_tasks": 9,
  "success": true,
  "tasks": [
    {
      "calendar_id": 1,
      "color": "#FF4848",
      "date_created": "2020-07-23, 23:55:40",
      "date_modified": "2020-07-26, 00:27:05",
      "details": "Shift 2 task",
      "end_time": "2020-07-25, 00:00:00",
      "id": 2,
      "is_all_day": true,
      "is_recurrent": false,
      "repetition_subtype": "",
      "repetition_type": "",
      "repetition_value": 0,
      "start_time": "2020-07-25, 00:00:00",
      "title": "Task 2"
    },
    {
      "calendar_id": 1,
      "color": "#2966B8",
      "date_created": "2020-07-23, 23:55:40",
      "date_modified": "2020-07-26, 11:33:11",
      "details": "FSND final project last day",
      "end_time": "2020-07-30, 00:00:00",
      "id": 3,
      "is_all_day": true,
      "is_recurrent": false,
      "repetition_subtype": "",
      "repetition_type": "",
      "repetition_value": 0,
      "start_time": "2020-07-30, 00:00:00",
      "title": "Final project date"
    },
    {
      "calendar_id": 1,
      "color": "#B05F3C",
      "date_created": "2020-07-26, 11:02:39",
      "date_modified": "2020-07-26, 15:32:40",
      "details": "Do something interesting",
      "end_time": "2020-07-31, 14:00:00",
      "id": 9,
      "is_all_day": false,
      "is_recurrent": false,
      "repetition_subtype": "",
      "repetition_type": "",
      "repetition_value": 0,
      "start_time": "2020-07-31, 12:00:00",
      "title": "🏖️ Something interesting"
    },
    {
      "calendar_id": 1,
      "color": "#2966B8",
      "date_created": "2020-08-01, 15:59:46",
      "date_modified": "2020-08-01, 15:59:46",
      "details": "Testing curl",
      "end_time": "2020-08-01, 23:59:59",
      "id": 18,
      "is_all_day": true,
      "is_recurrent": false,
      "repetition_subtype": "",
      "repetition_type": "",
      "repetition_value": 0,
      "start_time": "2020-08-01, 00:00:00",
      "title": "Test Task"
    },
    {
      "calendar_id": 1,
      "color": "#2966B8",
      "date_created": "2020-08-03, 09:31:32",
      "date_modified": "2020-08-04, 18:17:29",
      "details": "New task asaascsc",
      "end_time": "2020-08-28, 23:59:00",
      "id": 19,
      "is_all_day": true,
      "is_recurrent": false,
      "repetition_subtype": "",
      "repetition_type": "",
      "repetition_value": 0,
      "start_time": "2020-08-28, 00:00:00",
      "title": "New task asaascsc"
    },
    {
      "calendar_id": 1,
      "color": "#B19CDA",
      "date_created": "2020-07-23, 23:55:40",
      "date_modified": "2020-07-23, 23:55:40",
      "details": "Shift 1 task",
      "end_time": "2020-06-30, 00:00:00",
      "id": 1,
      "is_all_day": true,
      "is_recurrent": true,
      "repetition_subtype": "m",
      "repetition_type": "m",
      "repetition_value": 1,
      "start_time": "2020-06-30, 00:00:00",
      "title": "Task 1"
    },
    {
      "calendar_id": 1,
      "color": "#3EB34F",
      "date_created": "2020-07-24, 17:42:32",
      "date_modified": "2020-07-24, 17:42:32",
      "details": "Recurrent monthly task on Monday",
      "end_time": "2020-07-24, 23:59:59",
      "id": 4,
      "is_all_day": true,
      "is_recurrent": true,
      "repetition_subtype": "w",
      "repetition_type": "m",
      "repetition_value": 0,
      "start_time": "2020-07-24, 00:00:00",
      "title": "Recurrent"
    },
    {
      "calendar_id": 1,
      "color": "#2966B8",
      "date_created": "2020-07-24, 17:57:21",
      "date_modified": "2020-07-24, 17:57:21",
      "details": "Recurrent task weekly on Tuesday",
      "end_time": "2020-07-24, 23:59:59",
      "id": 6,
      "is_all_day": true,
      "is_recurrent": true,
      "repetition_subtype": "w",
      "repetition_type": "w",
      "repetition_value": 1,
      "start_time": "2020-07-24, 00:00:00",
      "title": "Recurrent Tuesday"
    },
    {
      "calendar_id": 1,
      "color": "#9588EC",
      "date_created": "2020-07-24, 17:59:17",
      "date_modified": "2020-07-24, 17:59:17",
      "details": "Recurrent monthly on day 15",
      "end_time": "2020-07-24, 23:59:59",
      "id": 7,
      "is_all_day": true,
      "is_recurrent": true,
      "repetition_subtype": "m",
      "repetition_type": "m",
      "repetition_value": 15,
      "start_time": "2020-07-24, 00:00:00",
      "title": "Recurrent"
    }
  ],
  "year": 2020
}
```

### GET /calendars/tasks/<int:task_id>/
- General:
  - Gets the tasks indicated by its id.
  - Returns a dictionary with the tasks, the calendar to which the task belongs to and success true
- Sample: `curl http://127.0.0.1:5000/api/calendars/tasks/1/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" | jq .`
- On success
```json
{
  "calendar": {
    "auto_decorate_task_details_hyperlink": true,
    "date_created": "2020-07-23, 23:55:40",
    "date_modified": "2020-08-05, 19:26:19",
    "days_past_to_keep_hidden_tasks": 62,
    "description": "Main floor emplyees calendar",
    "emojis_enabled": true,
    "hide_past_tasks": true,
    "id": 1,
    "max_year": 2200,
    "min_year": 2000,
    "name": "Main floor calendar",
    "show_view_past_btn": true,
    "time_zone": "Europe/Madrid",
    "week_starting_day": 0
  },
  "success": true,
  "task": {
    "calendar_id": 1,
    "color": "#B19CDA",
    "date_created": "2020-07-23, 23:55:40",
    "date_modified": "2020-07-23, 23:55:40",
    "details": "Shift 1 task",
    "end_time": "2020-06-30, 00:00:00",
    "id": 1,
    "is_all_day": true,
    "is_recurrent": true,
    "repetition_subtype": "m",
    "repetition_type": "m",
    "repetition_value": 1,
    "start_time": "2020-06-30, 00:00:00",
    "title": "Task 1"
  }
}
```

### POST /calendars/tasks/
- General:
  - Creates a new tasks, which will be associated to a specific calendar indicated by task.calendar_id.
  - Returns a dictionary with the tasks id, the calendar id to which the task belongs to and success true
- Sample: `curl http://localhost:5000/api/calendars/tasks/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" -d '{"calendar_id": 1, "title": "Test Task", "color": "#2966B8", "details": "Testing curl", "start_time": "2020-08-01, 00:00:00", "end_time": "2020-08-01, 23:59:59", "is_all_day": true, "is_recurrent": false, "repetition_value": 0, "repetition_type": "", "repetition_subtype": ""}' | jq .`
- On success:
```json
{
  "calendar_id": 1,
  "success": true,
  "task_id": 25
}
```

### PATCH /calendars/tasks/<int:task_id>/
- General:
  - Modifies an existing task's day by its task id. This is used to drag a task in the fronend to a new day in the calendar.
  - Returns the task id and succes true
- Sample: `curl http://localhost:5000/api/calendars/tasks/25/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" -d '{"newDay": 2}' -X PATCH | jq .`
- On succes:
```json
{
  "success": true,
  "task_id": 25
}
```

### DELETE /calendars/tasks/<int:task_id>/
- General:
  - Deletes an existing task's by its task id.
  - Returns a dictionary with the deleted task id, the task title and success true
- Sample: `curl http://localhost:5000/api/calendars/tasks/25/ -H "content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA" -X DELETE | jq .`
- On succes:
```json
{
  "success": true,
  "task_id": 25,
  "title": "Test Task"
}
```
