# FSND-calendar-backend
Backend application for the Capstone project, Udacity Full Stack Nano Degree

# Heroku deplyoment

The backend application can be deployed to Heroku following the next steps.

## Create Heroku app

To create the application, calendar-backend-acv, run the following command:

```
% heroku create calendar-backend-acv
Creating ⬢ calendar-backend-acv... done
https://calendar-backend-acv.herokuapp.com/ | https://git.heroku.com/calendar-backend-acv.git
```
## Add git remote for Heroku to local repository

Now we need to add a git remote to the Heroku Git:

```
% git remote add heroku https://git.heroku.com/calendar-backend-acv.git
```

## Add postgresql add on for our database

The last step is to create a postgresql database for the application:

```
% heroku addons:create heroku-postgresql:hobby-dev --app calendar-backend-acv
Creating heroku-postgresql:hobby-dev on ⬢ calendar-backend-acv... free
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
```

```
heroku config --app calendar-backend-acv
=== calendar-backend-acv Config Vars
DATABASE_URL: postgres://fvlgncowlnwdci:8db3311b2d1363b4a62c0729673aca8f72d33cb685a099b21795b0ad15c6d947@ec2-54-243-67-199.compute-1.amazonaws.com:5432/dadeus8j8nhtin
```

The database URL will be available in Hekoku through the enviroment variable DATABASE_URL that will be used by the application.

## Push the application

To actually deploy the application we have to push it into the Heroku Git. We can use the script herokuDeployment.sh

```
% ./herokuDeployment.sh
```

## Run migrations

Now we need to run the migrations to initialize the database

```
% heroku run python manage.py db upgrade --app calendar-backend-acv
Running python manage.py db upgrade on ⬢ calendar-backend-acv... up, run.3502 (Free)
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 437ef732aa0e, Initial migration.
INFO  [alembic.runtime.migration] Running upgrade 437ef732aa0e -> 91aac5980055, Remove User model
```

## Test the application

We can run the following curl command to test if the application is running.

```
% curl https://calendar-backend-acv.herokuapp.com/api/calendars/ -H "content-type: application/json" -X GET
```

We should get the following json:

``` json
{
  "calendars": [
    "{\"id\": 1, \"date_created\": \"2020-08-05, 20:26:33\", \"date_modified\": \"2020-08-05, 20:26:33\", \"name\": \"Main floor calendar\", \"description\": \"Main floor emplyees calendar\", \"min_year\": 2000, \"max_year\": 2200, \"time_zone\": \"Europe/Madrid\", \"week_starting_day\": 0, \"emojis_enabled\": true, \"show_view_past_btn\": true, \"auto_decorate_task_details_hyperlink\": true, \"hide_past_tasks\": false, \"days_past_to_keep_hidden_tasks\": 62}"
  ],
  "n_calendars": 1,
  "success": true
}
```
