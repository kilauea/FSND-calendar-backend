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

# Role: CalendarAdmin
# Permissions:
#   "delete:calendars",
#   "delete:tasks",
#   "get:calendars",
#   "get:tasks",
#   "patch:calendars",
#   "patch:tasks",
#   "post:calendars",
#   "post:tasks"
#
jwt_admin = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYWVkOTVmZGMzMjA2MGJlN2Y3ZTBjYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MDMyLCJleHAiOjE1OTkzMTgwMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcnMiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.YfJJSDmbi5N33LiUmHt10xAI4u-AWP1ium6MWYYUTFLMSoL5iZmFFMfLft4og3mrryBGgQ21Zu8W_Gw9Efxx44mgUG5eVweN4cBt158hqrrfOrcaJr1yRzJcL9FNpJ524MCahUero5mqhTFWDXMLt-izQBPBQ2TphRJixOO9Ig1WEfLCnc4zn6jDmkD0jhUv7vzVt3-3QMevB43Lr1fQAHskEk851WW6JVTsUJFzDHW04nOi7ZyTpAm1wO5aK2oUjOvGDZPDyaNepTZdVbVEsGvdjwoM2msbNwiaH_3M25o_JzE298M0AdYLlGoRIMrUiOa0bEK0Au6SGBf1XaeuRA'

# Role: CalendarManager
# Permissions:
#   "delete:tasks",
#   "get:calendars",
#   "get:tasks",
#   "patch:tasks",
#   "post:tasks"
#
jwt_manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYjM0MzRkZDhiMmJmMGMwNDVmYmZjYiIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MTg1LCJleHAiOjE1OTkzMTgxODUsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp0YXNrcyIsImdldDpjYWxlbmRhcnMiLCJnZXQ6dGFza3MiLCJwYXRjaDp0YXNrcyIsInBvc3Q6dGFza3MiXX0.mrwrzu32X-GRwsamSXBxzANVBANSirazCokQVeyRBDQTRX3BbVTxE7z7tY1YvZSMAJhPSnXmmr6B7eyuoqTbmirbW-RQNlQfiBxPOE5tk_ss--VzQ8_o2JXahBOJ9XQw_5sI7S1w-OOpqF_ttEr4RLWj39JkeeRAdnJ_YJXe9mVR7aNKX_ua8n7Ak-pLTyI8r9TpkdjvxPeffTZTsuFjMebR9Vp-LtHIMeTHRCSd6BVHXnqWeX7-zf_r0jwgWTh2Qfbtl9jwFnLPUgVG26VV8SnZXVL1Go6QjXzHKWKNraqr9TlzlO5FxYV9jDkbe9RtqQELvwdW6bAbkDGp4JGnAg'

# Role: CalendarUser
# Permissions:
#   "get:calendars",
#   "get:tasks"
#
jwt_user = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYjgzZThjNThiZGI1MGJmMjAyODdhYSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk2NzI2MjMyLCJleHAiOjE1OTkzMTgyMzIsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDpjYWxlbmRhcnMiLCJnZXQ6dGFza3MiXX0.UUUQ18JHLQL9YxWDuUX_gxQKxLNWfowinpTKLZgsPO_W2hhdQM663XqK19rYNcZ8DkH6CcHVkyBPQ_Y2B1GY7OA8qzSgfCgibZhnp24uJdPSNvUsoof7KNDwZAJXbpT2cAQ6hw7N9lJJpd_9chMllKLf5UoKWdAwzIlT6It8PE3lDM4fIIjLVK-7B3jIgw5pMe2_xRGprloKB4N4K-5jHgtmrKxj4B87N99ReTB99sG_iiBHHLpQeGJCcAaw86yyvX4UyUaXQPF4A_1V5176iRlVI13SfLGX4ObyouJTALDl2SprSXwDQ8Ii_5WMnyjUNrt0bcsCsAyhOKjHCIDR9A'


class CalendarTestCase(unittest.TestCase):
    """This class represents the Calendar test case"""

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

    def get_rbac_headers(self, role=None):
        headers = {'content-type': 'application/json'}
        if role == 'admin':
            headers['Authorization'] = 'Bearer %s' % jwt_admin
        elif role == 'manager':
            headers['Authorization'] = 'Bearer %s' % jwt_manager
        elif role == 'user':
            headers['Authorization'] = 'Bearer %s' % jwt_user
        return headers

    def check_no_authorization(self, json):
        self.assertEqual(json['success'], False)
        self.assertEqual(json['error'], 401)
        self.assertEqual(json['message'], 'Authorization header is expected.')

    def check_no_permissions(self, json):
        self.assertEqual(json['success'], False)
        self.assertEqual(json['error'], 401)
        self.assertEqual(json['message'], 'Permission not found.')

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
        @auth.requires_auth('post:calendars')
        def post_calendar(jwt):
    '''
    def test_post_calendar_no_jwt_error(self):
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
        self.check_no_authorization(res.json)

    def test_post_calendar_admin(self):
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
        res = self.client().post('/api/calendars/', json=calendar, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertTrue(res.json['calendar_id'] > 15)

    def test_post_calendar_admin_invalid_post_format(self):
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
        res = self.client().post('/api/calendars/', data=calendar, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)

    def test_post_calendar_manager_error(self):
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
        res = self.client().post('/api/calendars/', json=calendar, headers=self.get_rbac_headers('manager'))
        self.check_no_permissions(res.json)

    def test_post_calendar_user_error(self):
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
        res = self.client().post('/api/calendars/', json=calendar, headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['GET'])
        @auth.requires_auth('get:calendars')
        def get_calendar(jwt, calendar_id):
    '''
    def test_get_calendar_by_id_no_jwt_error(self):
        res = self.client().get('/api/calendars/1/')
        self.check_no_authorization(res.json)

    def test_get_calendar_by_id_admin(self):
        res = self.client().get('/api/calendars/1/', headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        calendar = res.json['calendar']
        self.assertTrue(type(calendar) == dict)
        self.assertTrue(calendar['name'] == 'Test Calendar 1')

    def test_get_calendar_by_id_manager(self):
        res = self.client().get('/api/calendars/1/', headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        calendar = res.json['calendar']
        self.assertTrue(type(calendar) == dict)
        self.assertTrue(calendar['name'] == 'Test Calendar 1')

    def test_get_calendar_by_id_user(self):
        res = self.client().get('/api/calendars/1/', headers=self.get_rbac_headers('user'))
        self.assertEqual(res.json['success'], True)
        calendar = res.json['calendar']
        self.assertTrue(type(calendar) == dict)
        self.assertTrue(calendar['name'] == 'Test Calendar 1')

    def test_get_calendar_invalid_id_admin(self):
        res = self.client().get('/api/calendars/1000/', headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['DELETE'])
        @auth.requires_auth('delete:calendars')
        def delete_calendar(jwt, calendar_id):
    '''
    def test_delete_calendar_by_id_no_jwt_error(self):
        calendar_id = 1
        res = self.client().delete('/api/calendars/%d/' % calendar_id)
        self.check_no_authorization(res.json)

    def test_delete_calendar_by_id_admin(self):
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
        res = self.client().delete('/api/calendars/%d/' % calendar.id, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['calendar_id'], calendar.id)

    def test_delete_calendar_by_id_manager_error(self):
        calendar_id = 1
        res = self.client().delete('/api/calendars/%d/' % calendar_id, headers=self.get_rbac_headers('manager'))
        self.check_no_permissions(res.json)

    def test_delete_calendar_by_id_user_error(self):
        calendar_id = 1
        res = self.client().delete('/api/calendars/%d/' % calendar_id, headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_delete_calendar_invalid_id_admin(self):
        calendar_id = 1000
        res = self.client().delete('/api/calendars/%d/' % calendar_id, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['calendar_id'], calendar_id)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['PATCH'])
        @auth.requires_auth('patch:calendars')
        def patch_calendar(jwt, calendar_id):
    '''
    def test_patch_calendar_by_id_no_jwt_error(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/', json={'name': new_name})
        self.check_no_authorization(res.json)

    def test_patch_calendar_by_id_admin(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/', json={'name': new_name}, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['name'], new_name)

    def test_patch_calendar_by_id_manager_error(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/', json={'name': new_name}, headers=self.get_rbac_headers('manager'))
        self.check_no_permissions(res.json)

    def test_patch_calendar_by_id_user_error(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/', json={'name': new_name}, headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_patch_calendar_invalid_id_admin(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1000/', json={'name': new_name}, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/tasks/', methods=['GET'])
        @auth.requires_auth('get:tasks')
        def get_tasks(jwt, calendar_id):
    '''
    def test_get_tasks_by_calendar_id_no_jwt_error(self):
        res = self.client().get('/api/calendars/1/tasks/')
        self.check_no_authorization(res.json)

    def test_get_tasks_by_calendar_id_admin(self):
        res = self.client().get('/api/calendars/1/tasks/', headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertTrue(type(res.json['calendar']) == dict)
        self.assertTrue(type(res.json['tasks']) == list)

    def test_get_tasks_by_calendar_id_manager(self):
        res = self.client().get('/api/calendars/1/tasks/', headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        self.assertTrue(type(res.json['calendar']) == dict)
        self.assertTrue(type(res.json['tasks']) == list)

    def test_get_tasks_by_calendar_id_user(self):
        res = self.client().get('/api/calendars/1/tasks/', headers=self.get_rbac_headers('user'))
        self.assertEqual(res.json['success'], True)
        self.assertTrue(type(res.json['calendar']) == dict)
        self.assertTrue(type(res.json['tasks']) == list)

    def test_get_tasks_invalid_calendar_id_admin(self):
        res = self.client().get('/api/calendars/1000/tasks/', headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/tasks/', methods=['POST'])
        @auth.requires_auth('post:tasks')
        def post_task(jwt):
    '''
    def test_post_task_no_jwt_error(self):
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
        self.check_no_authorization(res.json)

    def test_post_task_admin(self):
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
        res = self.client().post('/api/calendars/tasks/', json=task, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)

    def test_post_task_manager(self):
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
        res = self.client().post('/api/calendars/tasks/', json=task, headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)

    def test_post_task_user_error(self):
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
        res = self.client().post('/api/calendars/tasks/', json=task, headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_post_task_invalid_calendar_id_admin(self):
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
        res = self.client().post('/api/calendars/tasks/', json=task, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)

    '''
        @mod_api.route('/calendars/tasks/<int:task_id>/', methods=['GET'])
        @auth.requires_auth('get:tasks')
        def get_task(jwt, task_id):
    '''
    def test_get_task_by_id_no_jwt_error(self):
        id = 1
        res = self.client().get('/api/calendars/tasks/%d/' % id)
        self.check_no_authorization(res.json)

    def test_get_task_by_id_admin(self):
        id = 1
        res = self.client().get('/api/calendars/tasks/%d/' % id, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task']['id'], id)

    def test_get_task_by_id_manager(self):
        id = 1
        res = self.client().get('/api/calendars/tasks/%d/' % id, headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task']['id'], id)

    def test_get_task_by_id_user(self):
        id = 1
        res = self.client().get('/api/calendars/tasks/%d/' % id, headers=self.get_rbac_headers('user'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task']['id'], id)

    def test_get_task_invalid_id_admin(self):
        id = 1000
        res = self.client().get('/api/calendars/tasks/%d/' % id, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['task_id'], id)

    '''
        @mod_api.route('/calendars/tasks/<int:task_id>/', methods=['PATCH'])
        @auth.requires_auth('patch:tasks')
        def update_task_day(jwt, task_id):
    '''
    def test_patch_task_day_by_id_no_jwt_error(self):
        id = 1
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' % id, json={'newDay': new_day})
        self.check_no_authorization(res.json)

    def test_patch_task_day_by_id_admin(self):
        id = 1
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' % id, json={'newDay': new_day}, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_patch_task_day_by_id_manager(self):
        id = 1
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' % id, json={'newDay': new_day}, headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_patch_task_day_by_id_user_error(self):
        id = 1
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' % id, json={'newDay': new_day}, headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_patch_task_invalid_id_admin(self):
        id = 1000
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' % id, json={'newDay': new_day}, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['task_id'], id)

    '''
    @mod_api.route('/calendars/tasks/<int:task_id>/', methods=['DELETE'])
    @auth.requires_auth('delete:tasks')
    def delete_task(jwt, task_id):
    '''
    def test_delete_task_by_id_no_jwt_error(self):
        id = 1
        res = self.client().delete('/api/calendars/tasks/%d/' % id)
        self.check_no_authorization(res.json)

    def test_delete_task_by_id_admin(self):
        id = 1
        res = self.client().delete('/api/calendars/tasks/%d/' % id, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_delete_task_by_id_manager(self):
        id = 1
        res = self.client().delete('/api/calendars/tasks/%d/' % id, headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_delete_task_by_id_user_error(self):
        id = 1
        res = self.client().delete('/api/calendars/tasks/%d/' % id, headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_delete_task_invalid_id_admin(self):
        id = 1000
        res = self.client().delete('/api/calendars/tasks/%d/' % id, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['task_id'], id)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
