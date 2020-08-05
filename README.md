# FSND-calendar-backend
Back end application for the Capstone project, Udacity  Full Stack Nano Degree

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
% herokuDeployment.sh
```
