import sys
import json
import requests
from flask import (
    Blueprint,
    current_app,
    jsonify,
    request
)
from datetime import date, datetime, timedelta

from app.mod_api.models import Calendar
from app.mod_api.models import Task
import app.mod_auth.auth as auth

# Define the blueprint: 'api', set its url prefix: app.url/api
mod_api = Blueprint('api', __name__, url_prefix='/api')

@mod_api.route('/calendars/', methods=['GET'])
def get_calendars_list():
    calendars_query = Calendar.query.order_by(Calendar.date_created.desc()).paginate(error_out=False, max_per_page=10)
    if calendars_query.items:
        return jsonify({
            'success': True,
            'calendars' : [calendar.long() for calendar in calendars_query.items],
            'n_calendars': len(calendars_query.items)
        })
    else:
        return jsonify({
            'success': False,
            'n_calendars': 0
        })

@mod_api.route('/calendars/', methods=['POST'])
@auth.requires_auth('post:calendars')
def post_calendar(jwt):
    try:
        calendar = Calendar(**request.json)
        calendar.insert()
        return jsonify({
            'success': True,
            'calendar_id' : calendar.id
        })
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        pass
    return jsonify({
        'success': False
    })

@mod_api.route('/calendars/<int:calendar_id>/', methods=['GET'])
@auth.requires_auth('get:calendars')
def get_calendar(jwt, calendar_id):
    try:
        calendar = Calendar.query.get(calendar_id)
        if calendar:
            return jsonify({
                'success': True,
                'calendar': calendar.long()
            })
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        pass
    return jsonify({
        'success': False,
        'calendar_id': calendar_id
    })

@mod_api.route('/calendars/<int:calendar_id>/', methods=['DELETE'])
@auth.requires_auth('delete:calendars')
def delete_calendar(jwt, calendar_id):
    try:
        calendar = Calendar.query.get(calendar_id)
        if calendar:
            name = calendar.name
        else:
            return jsonify({
                'success': False,
                'calendar_id': calendar_id
            })
        calendar.delete()
        return jsonify({
            'success': True,
            'calendar_id': calendar_id,
            'name': name
        })
    except:
        #import traceback
        #print("Unexpected error:", sys.exc_info()[0])
        #traceback.print_exc(file=sys.stdout)
        return jsonify({
            'success': False,
            'calendar_id': calendar_id
        })

@mod_api.route('/calendars/<int:calendar_id>/', methods=['PATCH'])
@auth.requires_auth('patch:calendars')
def patch_calendar(jwt, calendar_id):
    try:
        calendar = Calendar.query.get(calendar_id)
        if calendar:
            for key, value in request.json.items():
                if key != 'id':
                    setattr(calendar, key, value)
            calendar.update()
            return jsonify({
                'success': True,
                'calendar_id': calendar_id,
                'name': calendar.name
            })
        else:
            return jsonify({
                'success': False,
                'calendar_id': calendar_id
            })
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return jsonify({
            'success': False,
            'calendar_id': calendar_id
        })

@mod_api.route('/calendars/<int:calendar_id>/tasks/', methods=['GET'])
@auth.requires_auth('get:tasks')
def get_tasks(jwt, calendar_id):
    calendar_query = Calendar.query.get(calendar_id)
    if calendar_query is None:
        return jsonify({
            'success': False,
            'calendar_id': calendar_id
        })

    today_date = datetime.date(datetime.now())
    current_day = today_date.day
    current_month = today_date.month
    current_year = today_date.year
    year = int(request.args.get("y", current_year))
    year = max(min(year, calendar_query.max_year), calendar_query.min_year)
    month = int(request.args.get("m", current_month))
    month = max(min(month, 12), 1)

    tasks = Task.getTasks(calendar_id, year, month, calendar_query.hide_past_tasks)

    return jsonify({
        'year': year,
        'month': month,
        'calendar': calendar_query.long(),
        'tasks': tasks,
        'n_tasks': len(tasks),
        'success': True
    })

@mod_api.route('/calendars/tasks/<int:task_id>/', methods=['GET'])
@auth.requires_auth('get:tasks')
def get_task(jwt, task_id):
    try:
        task_query = Task.query.join(Calendar).filter(Task.id == task_id).one_or_none()
        return jsonify({
            'success': True,
            'calendar': task_query.calendar.long(),
            'task': task_query.long()
        })
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return jsonify({
            'success': False,
            'task_id': task_id
        })

@mod_api.route('/calendars/tasks/', methods=['POST'])
@auth.requires_auth('post:tasks')
def post_task(jwt):
    try:
        newTask = request.json
        task = Task(**newTask)
        task.insert()
        return jsonify({
            'success': True,
            'calendar_id': task.calendar_id,
            'task_id': task.id
        })
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return jsonify({
            'success': False,
            'calendar_id': newTask['calendar_id']
        })

@mod_api.route('/calendars/tasks/<int:task_id>/', methods=['PATCH'])
@auth.requires_auth('patch:tasks')
def update_task_day(jwt, task_id):
    body = request.get_json()
    newDay = body.get('newDay', None)
    ret = False
    try:
        task = Task.getTask(task_id)
        if task and newDay:
            task.start_time = task.start_time.replace(day = int(newDay))
            task.end_time = task.end_time.replace(day = int(newDay))
            task.update()
            ret = True
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        pass

    return jsonify({
      'success': ret,
      'task_id': task_id
    })

@mod_api.route('/calendars/tasks/<int:task_id>/', methods=['DELETE'])
@auth.requires_auth('delete:tasks')
def delete_task(jwt, task_id):
    try:
        task = Task.getTask(task_id)
        if task:
            title = task.title
        else:
            return jsonify({
                'success': False,
                'task_id': task_id
            })
        task.delete()
        return jsonify({
            'success': True,
            'task_id': task_id,
            'title': title
        })
    except:
        return jsonify({
            'success': False,
            'task_id': task_id
        })

## Error Handling
'''
Error handler for unprocessable entity
'''
@mod_api.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
Error handler for 404
'''
@mod_api.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404

'''
Error handler for 400: bad request
'''
@mod_api.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
    }), 400
