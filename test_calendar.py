import os
import sys
import unittest
import json
from flask import session
import uuid
from datetime import datetime, timedelta

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
jwt_admin = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHR\
EdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6Im\
F1dGgwfDVmMzA0ZGQ5ODQ0NDUwMDAzZDkwODU2MSIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi\
8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk4NjI0MzU0LCJleHAiOj\
E2MDEyMTYzNTQsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcG\
UiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYWxlbmRhcn\
MiLCJkZWxldGU6dGFza3MiLCJnZXQ6Y2FsZW5kYXJzIiwiZ2V0OnRhc2tzIiwicGF0Y2g6Y2FsZW\
5kYXJzIiwicGF0Y2g6dGFza3MiLCJwb3N0OmNhbGVuZGFycyIsInBvc3Q6dGFza3MiXX0.teCNr8\
jk8sjhFF1jPwoKqtTeOVq5ZLOzzB6kBQeV7wG48g71xPnwnTWopQ0wmHsO4KdsptIKHZ5lie5-0W\
Bh7z9ibPPPNVodmVtZpyCHQRHOgXJH6-uHMLz6llhywVPmqq-oopd3_xrS50rtxmiqtwBIXiZBcw\
LKO9y3IWwlJHP56_72camSUxpT7TxWMnXcmKHHNmERTfazSRIcQxV-J9ZkZRioK5uxVGMro8uXDL\
Qfg77LUyzAoiUwBBoAFZjnne2tQdcg0cyTiy6gw5-XdwkaX6JDZCEa8J8juxlMXIOLwf6gxt94qU\
Jh2xPpKL814ZUpagvm_YVFbO33aWcSFw'

# Role: CalendarManager
# Permissions:
#   "delete:tasks",
#   "get:calendars",
#   "get:tasks",
#   "patch:tasks",
#   "post:tasks"
#
jwt_manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEd\
HREdHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6\
ImF1dGgwfDVmMzA1M2RkMWM0NGRjMDAzNzUxNzUzOCIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBz\
Oi8va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk4NjI0NDY5LCJleHAi\
OjE2MDEyMTY0NjksImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2Nv\
cGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp0YXNrcyIs\
ImdldDpjYWxlbmRhcnMiLCJnZXQ6dGFza3MiLCJwYXRjaDp0YXNrcyIsInBvc3Q6dGFza3MiXX0.\
G9Lo0A8-tuTURiNFnDBbeXeu7hqtG6eZUtOhbshfQU7joubCPazPk_teG2pYzsnqbQQ7qA9j9HSj\
f9QxqO6zbU21IdjeOxiHx-rtpSBYIQYrl1bmJM6JL488M_Rg5zy6elHuuW1ZHo1D5PskQJT_utOZ\
6wCvcB3qRAEqsjFBxze3JCuNk2Gh0oDtiTMTAD8eoEj2P6Vonme6Kj340ZjZ7wWHaUV7g-PDKl0q\
TgKKD3CfJtz9v2v_lwz1Eij6x2BRD0Q3nuVPC0QDut5wkyeHKbZYgGdzewX2TqIH5P2B6xEtDcSS\
GsPVPCuMKcQijbVi5Ow3CAdpysS0zte_xrCPag'

# Role: CalendarUser
# Permissions:
#   "get:calendars",
#   "get:tasks"
#
jwt_user = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVFUkJESDlzMHZEdHRE\
dHl6WkRVNSJ9.eyJpc3MiOiJodHRwczovL2tpbGF1ZWEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF\
1dGgwfDVmMzA1NDI4NTBhNWU1MDAzNzQwNTRiYyIsImF1ZCI6WyJjYWxlbmRhciIsImh0dHBzOi8\
va2lsYXVlYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk4NjI0NTE2LCJleHAiOjE\
2MDEyMTY1MTYsImF6cCI6Im9yUTBZTnlJdEhwWkhWQXdwRzJQYVJNV2pMODJxSndnIiwic2NvcGU\
iOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDpjYWxlbmRhcnMiLCJ\
nZXQ6dGFza3MiXX0.eEMgV7FDOo2D2ZsHVbVgxmC_389hbmCftDio2YXCsRfubvlqR0ZlH4tlAoy\
9w0tIKDCCrM9IKLq1fbqJ6rYZdAdlab1csIInqDbiSGIleSMk_3ecNE5RvmUSx_rc6DjXt6tLlfj\
gCJ022-FbdCcUjquIzpv4-G2ciEv3B1sS4n13dnsYlAJKRUn0zqrXke4xL6kJcoMz9XQFFid2dCB\
ybB0iCr51BVwlX7mC30DacY9LtMtrelO6F7b0h2qjuQT17B8GPEMRh2SDdPRm5HscsdHUk7z9Vi0\
iJN4S66UwAc1hM3cVSeL1MeIkAukdPsx8ZLDBy-664kLK3cIJLzOEIw'


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
                name='Test Calendar %d' % (i + 1),
                description='Test Calendar %d' % (i + 1),
                min_year=2000,
                max_year=2050,
                time_zone='Europe/Madrid',
                week_starting_day=0,
                emojis_enabled=True,
                show_view_past_btn=True
            )
            calendar.insert()
            for t in range(self.n_tasks):
                task = Task(
                    calendar_id=calendar.id,
                    title='Test Task %d' % t,
                    color='#B19CDA',
                    details='Test Task %d' % t,
                    start_time=datetime.now() + timedelta(days=t - 5),
                    end_time=datetime.now() + timedelta(days=t - 5),
                    is_all_day=True,
                    is_recurrent=False,
                    repetition_value=0,
                    repetition_type=' ',
                    repetition_subtype=' '
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
        res = self.client().post('/api/calendars/', json=calendar,
                                 headers=self.get_rbac_headers('admin'))
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
        res = self.client().post('/api/calendars/', data=calendar,
                                 headers=self.get_rbac_headers('admin'))
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
        res = self.client().post('/api/calendars/', json=calendar,
                                 headers=self.get_rbac_headers('manager'))
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
        res = self.client().post('/api/calendars/', json=calendar,
                                 headers=self.get_rbac_headers('user'))
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
        res = self.client().get('/api/calendars/1/',
                                headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        calendar = res.json['calendar']
        self.assertTrue(type(calendar) == dict)
        self.assertTrue(calendar['name'] == 'Test Calendar 1')

    def test_get_calendar_by_id_manager(self):
        res = self.client().get('/api/calendars/1/',
                                headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        calendar = res.json['calendar']
        self.assertTrue(type(calendar) == dict)
        self.assertTrue(calendar['name'] == 'Test Calendar 1')

    def test_get_calendar_by_id_user(self):
        res = self.client().get('/api/calendars/1/',
                                headers=self.get_rbac_headers('user'))
        self.assertEqual(res.json['success'], True)
        calendar = res.json['calendar']
        self.assertTrue(type(calendar) == dict)
        self.assertTrue(calendar['name'] == 'Test Calendar 1')

    def test_get_calendar_invalid_id_admin(self):
        res = self.client().get('/api/calendars/1000/',
                                headers=self.get_rbac_headers('admin'))
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
            name='Test Calendar to delete',
            description='Test Calendar to delete',
            min_year=2000,
            max_year=2050,
            time_zone='Europe/Madrid',
            week_starting_day=0,
            emojis_enabled=True,
            show_view_past_btn=True
        )
        calendar.insert()
        res = self.client().delete('/api/calendars/%d/' %
                                   calendar.id,
                                   headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['calendar_id'], calendar.id)

    def test_delete_calendar_by_id_manager_error(self):
        calendar_id = 1
        res = self.client().delete('/api/calendars/%d/' %
                                   calendar_id,
                                   headers=self.get_rbac_headers('manager'))
        self.check_no_permissions(res.json)

    def test_delete_calendar_by_id_user_error(self):
        calendar_id = 1
        res = self.client().delete('/api/calendars/%d/' %
                                   calendar_id,
                                   headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_delete_calendar_invalid_id_admin(self):
        calendar_id = 1000
        res = self.client().delete('/api/calendars/%d/' %
                                   calendar_id,
                                   headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['calendar_id'], calendar_id)

    '''
        @mod_api.route('/calendars/<int:calendar_id>/', methods=['PATCH'])
        @auth.requires_auth('patch:calendars')
        def patch_calendar(jwt, calendar_id):
    '''

    def test_patch_calendar_by_id_no_jwt_error(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/',
                                  json={'name': new_name})
        self.check_no_authorization(res.json)

    def test_patch_calendar_by_id_admin(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/',
                                  json={'name': new_name},
                                  headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['name'], new_name)

    def test_patch_calendar_by_id_manager_error(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/',
                                  json={'name': new_name},
                                  headers=self.get_rbac_headers('manager'))
        self.check_no_permissions(res.json)

    def test_patch_calendar_by_id_user_error(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1/',
                                  json={'name': new_name},
                                  headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_patch_calendar_invalid_id_admin(self):
        new_name = 'New calendar name'
        res = self.client().patch('/api/calendars/1000/',
                                  json={'name': new_name},
                                  headers=self.get_rbac_headers('admin'))
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
        res = self.client().get('/api/calendars/1/tasks/',
                                headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertTrue(type(res.json['calendar']) == dict)
        self.assertTrue(type(res.json['tasks']) == list)

    def test_get_tasks_by_calendar_id_manager(self):
        res = self.client().get('/api/calendars/1/tasks/',
                                headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        self.assertTrue(type(res.json['calendar']) == dict)
        self.assertTrue(type(res.json['tasks']) == list)

    def test_get_tasks_by_calendar_id_user(self):
        res = self.client().get('/api/calendars/1/tasks/',
                                headers=self.get_rbac_headers('user'))
        self.assertEqual(res.json['success'], True)
        self.assertTrue(type(res.json['calendar']) == dict)
        self.assertTrue(type(res.json['tasks']) == list)

    def test_get_tasks_invalid_calendar_id_admin(self):
        res = self.client().get('/api/calendars/1000/tasks/',
                                headers=self.get_rbac_headers('admin'))
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
        res = self.client().post('/api/calendars/tasks/', json=task,
                                 headers=self.get_rbac_headers('admin'))
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
        res = self.client().post('/api/calendars/tasks/', json=task,
                                 headers=self.get_rbac_headers('manager'))
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
        res = self.client().post('/api/calendars/tasks/', json=task,
                                 headers=self.get_rbac_headers('user'))
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
        res = self.client().post('/api/calendars/tasks/', json=task,
                                 headers=self.get_rbac_headers('admin'))
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
        res = self.client().get('/api/calendars/tasks/%d/' %
                                id, headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task']['id'], id)

    def test_get_task_by_id_manager(self):
        id = 1
        res = self.client().get('/api/calendars/tasks/%d/' %
                                id, headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task']['id'], id)

    def test_get_task_by_id_user(self):
        id = 1
        res = self.client().get('/api/calendars/tasks/%d/' %
                                id, headers=self.get_rbac_headers('user'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task']['id'], id)

    def test_get_task_invalid_id_admin(self):
        id = 1000
        res = self.client().get('/api/calendars/tasks/%d/' %
                                id, headers=self.get_rbac_headers('admin'))
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
        res = self.client().patch('/api/calendars/tasks/%d/' %
                                  id, json={'newDay': new_day})
        self.check_no_authorization(res.json)

    def test_patch_task_day_by_id_admin(self):
        id = 1
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' %
                                  id, json={'newDay': new_day},
                                  headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_patch_task_day_by_id_manager(self):
        id = 1
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' %
                                  id, json={'newDay': new_day},
                                  headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_patch_task_day_by_id_user_error(self):
        id = 1
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' %
                                  id, json={'newDay': new_day},
                                  headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_patch_task_invalid_id_admin(self):
        id = 1000
        new_day = 1
        res = self.client().patch('/api/calendars/tasks/%d/' %
                                  id, json={'newDay': new_day},
                                  headers=self.get_rbac_headers('admin'))
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
        res = self.client().delete('/api/calendars/tasks/%d/' %
                                   id,
                                   headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_delete_task_by_id_manager(self):
        id = 1
        res = self.client().delete('/api/calendars/tasks/%d/' %
                                   id,
                                   headers=self.get_rbac_headers('manager'))
        self.assertEqual(res.json['success'], True)
        self.assertEqual(res.json['task_id'], id)

    def test_delete_task_by_id_user_error(self):
        id = 1
        res = self.client().delete('/api/calendars/tasks/%d/' %
                                   id,
                                   headers=self.get_rbac_headers('user'))
        self.check_no_permissions(res.json)

    def test_delete_task_invalid_id_admin(self):
        id = 1000
        res = self.client().delete('/api/calendars/tasks/%d/' %
                                   id,
                                   headers=self.get_rbac_headers('admin'))
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['task_id'], id)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
