import os
import sys
import unittest
import json
from flask import session
import uuid
from datetime import datetime, timedelta
import pickle

from app import create_app, db
from app.mod_api.models import Calendar
from app.mod_api.models import Task

class CalendarTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('config_test')
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client
        # # apply any/all pending migrations.
        # with self.app.app_context():
        #     from flask_migrate import upgrade as _upgrade
        #     _upgrade(directory=os.path.join(os.path.dirname(__file__), 'migrations'))

        for i in range(15):
            calendar = Calendar(
                name = 'Test Calendar %d' % (i + 1),
                description = 'Test Calendar %d' % (i + 1),
                min_year = 2000,
                max_year = 2050,
                time_zone = 'Europe/Madrid',
                week_starting_day = 0,
                emojis_enabled = True,
                show_view_past_btn = True
            )
            calendar.insert()
            for t in range(15):
                task = Task(
                    calendar_id = calendar.id,
                    title = 'Test Task %d' % t,
                    color = '#B19CDA',
                    details = 'Test Task %d' % t,
                    start_time = datetime.now() + timedelta(days=t - 5),
                    end_time = datetime.now() + timedelta(days=t - 5),
                    is_all_day = True,
                    is_recurrent = False,
                    repetition_value = 0,
                    repetition_type = ' ',
                    repetition_subtype =  ' '
                )
                task.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
        @mod_api.route('/calendars/', methods=['GET'])
        def get_calendars_list():
    '''
    def test_get_calendars(self):
        res = self.client().get('/api/calendars/')
        self.assertEqual(res.json['success'], True)
        self.assertTrue(res.json['n_calendars'] > 0)

    def test_get_calendars_paginate(self):
        res = self.client().get('/api/calendars/?page=2')
        self.assertEqual(res.json['success'], True)
        self.assertTrue(res.json['n_calendars'] > 0)

    def test_get_calendars_paginate_error(self):
        res = self.client().get('/api/calendars/?page=10')
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['n_calendars'], 0)

    '''
        @mod_api.route('/calendars/', methods=['POST'])
        def post_calendar():
    '''

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['GET'])
        def get_calendar(calendar_id):
    '''

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['DELETE'])
        def delete_calendar(calendar_id):
    '''

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['PATCH'])
        def patch_calendar(calendar_id):
    '''

    '''
        @mod_api.route('/calendars/<int:calendar_id>/tasks/', methods=['GET'])
        def get_tasks(calendar_id):
    '''

    '''
        @mod_api.route('/calendars/<int:calendar_id>/tasks/', methods=['POST'])
        def post_task(calendar_id):
    '''

    '''
        @mod_api.route('/calendars/<int:calendar_id>/tasks/<int:task_id>/', methods=['GET'])
        def get_task(calendar_id, task_id):
    '''

    # def test_get_home_invalid_failed(self):
    #     res = self.client().get('/calendars')
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual('There\'s nothing here!' in res.data.decode(), True)

    # def test_get_ome_calendar_logged_in(self):
    #     with self.app.test_client() as client:
    #         self.login(client)
    #         res = client.get('/calendar/1/')
    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(res.mimetype,'text/html')
    #         self.assertIn('Calendar - Arturo Crespo de la Viña', res.data.decode())

    # def test_get_ome_calendar_logged_out(self):
    #     with self.app.test_client() as client:
    #         res = client.get('/calendar/1/')
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 401)
    #         self.assertEqual(data['success'], False)
    #         self.assertEqual(data['message'], 'Permission not found.')

    # def test_post_calendar_logged_in(self):
    #     with self.app.test_client() as client:
    #         self.login(client)
    #         form_data = {
    #             'name': 'Test Calendar',
    #             'description': str(uuid.uuid4()) + str(uuid.uuid4()),
    #             'min_year': 2000,
    #             'max_year': 2050,
    #             'time_zone': 'Europe/Madrid',
    #             'week_starting_day': 0,
    #             'emojis_enabled': True,
    #             'show_view_past_btn': True
    #         }
    #         res = client.post('/calendar/create', data=form_data)
    #         self.assertEqual(res.status_code, 302)
    #         self.assertIn('/calendar/', res.location)
    #         self.assertEqual(res.mimetype,'text/html')
    #         self.assertIn('You should be redirected automatically to target URL:', res.data.decode())
    #         query = Calendar.query.filter_by(description=form_data['description']).all()
    #         for calendar in query:
    #             calendar.delete()

    # def test_post_calendar_logged_out(self):
    #     with self.app.test_client() as client:
    #         form_data = {
    #             'name': 'Test Calendar',
    #             'description': str(uuid.uuid4()) + str(uuid.uuid4()),
    #             'min_year': 2000,
    #             'max_year': 2050,
    #             'time_zone': 'Europe/Madrid',
    #             'week_starting_day': 0,
    #             'emojis_enabled': True,
    #             'show_view_past_btn': True
    #         }
    #         res = client.post('/calendar/create', data=form_data)
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 401)
    #         self.assertEqual(data['success'], False)
    #         self.assertEqual(data['message'], 'Permission not found.')

    # def test_delete_calendar_logged_in(self):
    #     with self.app.test_client() as client:
    #         self.login(client)
    #         calendar = Calendar(
    #             name = 'Test Calendar',
    #             description = str(uuid.uuid4()) + str(uuid.uuid4()),
    #             min_year = 2000,
    #             max_year = 2050,
    #             time_zone = 'Europe/Madrid',
    #             week_starting_day = 0,
    #             emojis_enabled = True,
    #             show_view_past_btn = True
    #         )
    #         calendar.insert()
    #         res = client.delete('/calendar/%d/delete' % calendar.id)
    #         self.assertEqual(res.status_code, 302)
    #         self.assertIn('/calendar/', res.location)
    #         self.assertEqual(res.mimetype,'text/html')
    #         self.assertIn('You should be redirected automatically to target URL:', res.data.decode())
    #         query = Calendar.query.get(calendar.id)
    #         self.assertEqual(query, None)

    # def test_delete_calendar_logged_out(self):
    #     with self.app.test_client() as client:
    #         res = client.delete('/calendar/1/delete')
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 401)
    #         self.assertEqual(data['success'], False)
    #         self.assertEqual(data['message'], 'Permission not found.')

    # def test_get_calendar_tasks_logged_in(self):
    #     with self.app.test_client() as client:
    #         self.login(client)
    #         res = client.get('/calendar/1/tasks')
    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(res.mimetype,'text/html')

    # def test_get_calendar_tasks_logged_out(self):
    #     with self.app.test_client() as client:
    #         res = client.get('/calendar/1/tasks')
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 401)
    #         self.assertEqual(data['success'], False)
    #         self.assertEqual(data['message'], 'Permission not found.')

    # def test_post_calendar_tasks_logged_in(self):
    #     with self.app.test_client() as client:
    #         form_data = {
    #             'calendar_id': 1,
    #             'title': 'Test Task',
    #             'color': '#B19CDA',
    #             'details': str(uuid.uuid4()) + str(uuid.uuid4()),
    #             'start_time': datetime.now(),
    #             'end_time': datetime.now(),
    #             'is_all_day': True,
    #             'is_recurrent': False,
    #             'repetition_value': 0,
    #             'repetition_type': ' ',
    #             'repetition_subtype': ' '
    #         }
    #         self.login(client)
    #         res = client.post('/calendar/1/tasks', data=form_data)
    #         self.assertEqual(res.status_code, 302)
    #         #self.assertIn('/calendar/', res.location)
    #         self.assertEqual(res.mimetype,'text/html')
    #         self.assertIn('You should be redirected automatically to target URL:', res.data.decode())
    #         query = Task.query.filter_by(details=form_data['details']).all()
    #         for taks in query:
    #             taks.delete()

    # def test_post_calendar_tasks_logged_out(self):
    #     with self.app.test_client() as client:
    #         form_data = {
    #             'calendar_id': 1,
    #             'title': 'Test Task',
    #             'color': '#B19CDA',
    #             'details': str(uuid.uuid4()) + str(uuid.uuid4()),
    #             'start_time': datetime.now(),
    #             'end_time': datetime.now(),
    #             'is_all_day': True,
    #             'is_recurrent': False,
    #             'repetition_value': 0,
    #             'repetition_type': ' ',
    #             'repetition_subtype': ' '
    #         }
    #         res = client.post('/calendar/1/tasks', data=form_data)
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 401)
    #         self.assertEqual(data['success'], False)
    #         self.assertEqual(data['message'], 'Permission not found.')

    # def test_delete_calendar_tasks_logged_in(self):
    #     with self.app.test_client() as client:
    #         self.login(client)
    #         task = Task(
    #             calendar_id = 1,
    #             title = 'Test Task',
    #             color = '#B19CDA',
    #             details = str(uuid.uuid4()) + str(uuid.uuid4()),
    #             start_time = datetime.now(),
    #             end_time = datetime.now(),
    #             is_all_day = True,
    #             is_recurrent = False,
    #             repetition_value = 0,
    #             repetition_type = ' ',
    #             repetition_subtype =  ' '
    #         )
    #         task.insert()
    #         res = client.delete('/calendar/%d/tasks/%d' % (task.calendar_id, task.id))
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(data['success'], True)
    #         self.assertEqual(data['task_id'], task.id)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
