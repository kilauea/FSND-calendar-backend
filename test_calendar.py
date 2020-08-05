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

        self.n_calendars = 15
        self.n_tasks = 15

        for i in range(self.n_calendars):
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
            for t in range(self.n_tasks):
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
        self.assertTrue(res.json['n_calendars'] == 10)

    def test_get_calendars_paginate(self):
        res = self.client().get('/api/calendars/?page=2')
        self.assertEqual(res.json['success'], True)
        self.assertTrue(res.json['n_calendars'] == 5)

    def test_get_calendars_paginate_error(self):
        res = self.client().get('/api/calendars/?page=10')
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['n_calendars'], 0)

    '''
        @mod_api.route('/calendars/', methods=['POST'])
        def post_calendar():
    '''
    def test_post_calendar(self):
        calendar = {
            'name': 'Test Calendar Post',
            'description': 'Test Calendar Post',
            'min_year': 2000,
            'max_year': 2050,
            'time_zone': 'Europe/Madrid',
            'week_starting_day': 6,
            'emojis_enabled': True,
            'show_view_past_btn': True,
            'auto_decorate_task_details_hyperlink': True,
            'hide_past_tasks': False,
            'days_past_to_keep_hidden_tasks': 62
        }
        res = self.client().post('/api/calendars/', json=calendar)
        self.assertEqual(res.json['success'], True)
        self.assertTrue(res.json['calendar_id'] > 15)

    def test_post_calendar_invalid_post_format(self):
        calendar = {
            'name': 'Test Calendar Post',
            'description': 'Test Calendar Post',
            'min_year': 2000,
            'max_year': 2050,
            'time_zone': 'Europe/Madrid',
            'week_starting_day': 6,
            'emojis_enabled': True,
            'show_view_past_btn': True,
            'auto_decorate_task_details_hyperlink': True,
            'hide_past_tasks': False,
            'days_past_to_keep_hidden_tasks': 62
        }
        res = self.client().post('/api/calendars/', data=calendar)
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['GET'])
        def get_calendar(calendar_id):
    '''
    def test_get_calendar_by_id(self):
        res = self.client().get('/api/calendars/1/')
        self.assertEqual(res.json['success'], True)
        calendar = res.json['calendar']
        self.assertTrue(type(calendar) == dict)
        self.assertTrue(calendar['name'] == 'Test Calendar 1')

    def test_get_calendar_invalid_id(self):
        res = self.client().get('/api/calendars/1000/')
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['DELETE'])
        def delete_calendar(calendar_id):
    '''
    def test_delete_calendar_by_id(self):
        calendar = Calendar(
            name = 'Test Calendar to delete',
            description = 'Test Calendar to delete',
            min_year = 2000,
            max_year = 2050,
            time_zone = 'Europe/Madrid',
            week_starting_day = 0,
            emojis_enabled = True,
            show_view_past_btn = True
        )
        calendar.insert()
        res = self.client().delete('/api/calendars/%d/' % calendar.id)
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['calendar_id'], calendar.id)

    def test_delete_calendar_invalid_id(self):
        calendar_id = 1000
        res = self.client().delete('/api/calendars/%d/' % calendar_id)
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['calendar_id'], calendar_id)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['PATCH'])
        def patch_calendar(calendar_id):
    '''
    def test_patch_calendar_by_id(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/', json={'name': new_name})
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['name'], new_name)

    def test_patch_calendar_invalid_id(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1000/', json={'name': new_name})
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/tasks/', methods=['GET'])
        def get_tasks(calendar_id):
    '''
    def test_get_tasks_by_calendar_id(self):
        res = self.client().get('/api/calendars/1/tasks/')
        self.assertEqual(res.json['success'], True)
        self.assertTrue(type(res.json['calendar']) == dict)
        self.assertTrue(type(res.json['tasks']) == list)

    def test_get_tasks_invalid_calendar_id(self):
        res = self.client().get('/api/calendars/1000/tasks/')
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/tasks/', methods=['POST'])
        def post_task():
    '''
    def test_post_task(self):
        task = {
            'calendar_id': 1,
            'title': 'Test new Task',
            'color': '#B19CDA',
            'details': 'Test new Task',
            'start_time': datetime.now() + timedelta(days=1 - 5),
            'end_time': datetime.now() + timedelta(days=1 - 5),
            'is_all_day': True,
            'is_recurrent': False,
            'repetition_value': 0,
            'repetition_type': ' ',
            'repetition_subtype':  ' '
        }
        res = self.client().post('/api/calendars/tasks/', json=task)
        self.assertEqual(res.json['success'], True)

    def test_post_task_invalid_calendar_id(self):
        task = {
            'calendar_id': 1000,
            'title': 'Test new Task',
            'color': '#B19CDA',
            'details': 'Test new Task',
            'start_time': datetime.now() + timedelta(days=1 - 5),
            'end_time': datetime.now() + timedelta(days=1 - 5),
            'is_all_day': True,
            'is_recurrent': False,
            'repetition_value': 0,
            'repetition_type': ' ',
            'repetition_subtype':  ' '
        }
        res = self.client().post('/api/calendars/tasks/', json=task)
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/tasks/<int:task_id>/', methods=['GET'])
        def get_task(task_id):
    '''
    def test_get_task_by_id(self):
        id = 1
        res = self.client().get('/api/calendars/tasks/%d/' % id)
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task']['id'], id)

    def test_get_task_invalid_id(self):
        id = 1000
        res = self.client().get('/api/calendars/tasks/%d/' % id)
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['task_id'], id)

    '''
        @mod_api.route('/calendars/tasks/<int:task_id>/', methods=['PATCH'])
        def update_task_day(task_id):
    '''
    def test_patch_task_day_by_id(self):
        id = 1
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' % id, json={'newDay': new_day})
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_patch_task_invalid_id(self):
        id = 1000
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' % id, json={'newDay': new_day})
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['task_id'], id)

    '''
    @mod_api.route('/calendars/tasks/<int:task_id>/', methods=['DELETE'])
    def delete_task(task_id):
    '''
    def test_delete_task_by_id(self):
        id = 1
        res = self.client().delete('/api/calendars/tasks/%d/' % id)
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_delete_task_invalid_id(self):
        id = 1000
        res = self.client().delete('/api/calendars/tasks/%d/' % id)
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['task_id'], id)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
