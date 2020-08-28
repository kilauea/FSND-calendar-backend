# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from datetime import date, datetime, timedelta
from sqlalchemy import extract, and_
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app import db
import json
import calendar
from app.mod_base.base_model import Base


# Define a User model


class Calendar(Base):
    __tablename__ = 'calendar'
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    min_year = db.Column(db.SmallInteger, nullable=False, default=2000)
    max_year = db.Column(db.SmallInteger, nullable=False, default=2200)
    time_zone = db.Column(db.String(128), nullable=False,
                          default="Europe/Madrid")
    week_starting_day = db.Column(
        db.SmallInteger, nullable=False, default=0)      # 0: Monday, 6: Sunday
    emojis_enabled = db.Column(db.Boolean, nullable=False, default=True)
    auto_decorate_task_details_hyperlink = db.Column(
        db.Boolean, nullable=False, default=True)
    show_view_past_btn = db.Column(db.Boolean, nullable=False, default=True)
    hide_past_tasks = db.Column(db.Boolean, nullable=False, default=False)
    days_past_to_keep_hidden_tasks = db.Column(
        db.SmallInteger, nullable=False, default=62)

    def __init__(
        self,
        id=None,
        date_created=None,
        date_modified=None,
        name=None,
        description=None,
        min_year=None,
        max_year=None,
        time_zone=None,
        week_starting_day=None,
        emojis_enabled=None,
        show_view_past_btn=None,
        auto_decorate_task_details_hyperlink=True,
        hide_past_tasks=False,
        days_past_to_keep_hidden_tasks=62
    ):
        self.id = id
        if date_created:
            self.date_created = datetime.strptime(
                date_created, '%Y-%m-%d, %H:%M:%S')
        else:
            self.date_created = datetime.now()
        if date_modified:
            self.date_modified = datetime.strptime(
                date_modified, '%Y-%m-%d, %H:%M:%S')
        else:
            self.date_modified = datetime.now()
        self.name = name
        self.description = description
        self.min_year = min_year
        self.max_year = max_year
        self.time_zone = time_zone
        self.week_starting_day = week_starting_day
        self.emojis_enabled = emojis_enabled
        self.show_view_past_btn = show_view_past_btn
        self.auto_decorate_task_details_hyperlink = \
            auto_decorate_task_details_hyperlink
        self.hide_past_tasks = hide_past_tasks
        self.days_past_to_keep_hidden_tasks = \
            days_past_to_keep_hidden_tasks

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'date_created': self.date_created.strftime("%Y-%m-%d, %H:%M:%S"),
            'date_modified': self.date_modified.strftime("%Y-%m-%d, %H:%M:%S"),
            'name': self.name,
            'description': self.description,
            'min_year': self.min_year,
            'max_year': self.max_year,
            'time_zone': self.time_zone,
            'week_starting_day': self.week_starting_day,
            'emojis_enabled': self.emojis_enabled,
            'show_view_past_btn': self.show_view_past_btn,
            'auto_decorate_task_details_hyperlink':
            self.auto_decorate_task_details_hyperlink,
            'hide_past_tasks': self.hide_past_tasks,
            'days_past_to_keep_hidden_tasks':
            self.days_past_to_keep_hidden_tasks
        })

    def long(self):
        return {
            'id': self.id,
            'date_created':
            self.date_created.strftime("%Y-%m-%d, %H:%M:%S"),
            'date_modified':
            self.date_modified.strftime("%Y-%m-%d, %H:%M:%S"),
            'name': self.name,
            'description': self.description,
            'min_year': self.min_year,
            'max_year': self.max_year,
            'time_zone': self.time_zone,
            'week_starting_day': self.week_starting_day,
            'emojis_enabled': self.emojis_enabled,
            'show_view_past_btn': self.show_view_past_btn,
            'auto_decorate_task_details_hyperlink':
            self.auto_decorate_task_details_hyperlink,
            'hide_past_tasks': self.hide_past_tasks,
            'days_past_to_keep_hidden_tasks':
            self.days_past_to_keep_hidden_tasks
        }

    @staticmethod
    def previous_month_and_year(year, month):
        previous_month_date = date(year, month, 1) - timedelta(days=2)
        return previous_month_date.month, previous_month_date.year

    @staticmethod
    def next_month_and_year(year, month):
        last_day_of_month = calendar.monthrange(year, month)[1]
        next_month_date = date(
            year, month, last_day_of_month) + timedelta(days=2)
        return next_month_date.month, next_month_date.year

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        db.session.commit()


class Task(Base):
    __tablename__ = 'task'

    calendar_id = db.Column(db.Integer, db.ForeignKey(
        'calendar.id'), nullable=False)
    calendar = relationship("Calendar", back_populates="tasks")
    title = db.Column(db.String(128), nullable=False)
    color = db.Column(db.String(32), nullable=False)
    details = db.Column(db.String(256), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False,
                           default=func.current_timestamp())
    end_time = db.Column(db.DateTime, nullable=False,
                         default=func.current_timestamp())
    is_all_day = db.Column(db.Boolean, nullable=False, default=False)
    is_recurrent = db.Column(db.Boolean, nullable=False, default=False)
    repetition_value = db.Column(db.SmallInteger, nullable=False, default=0)
    repetition_type = db.Column(db.String(1), nullable=False, default="")
    repetition_subtype = db.Column(db.String(1), nullable=False, default="")

    def __init__(
        self,
        date_created=None,
        date_modified=None,
        calendar_id=None,
        title=None,
        color=None,
        details=None,
        start_time=None,
        end_time=None,
        is_all_day=None,
        is_recurrent=None,
        repetition_value=None,
        repetition_type=None,
        repetition_subtype=None
    ):
        self.calendar_id = calendar_id
        if date_created:
            self.date_created = datetime.strptime(
                date_created, '%Y-%m-%d, %H:%M:%S')
        else:
            self.date_created = datetime.now()
        if date_modified:
            self.date_modified = datetime.strptime(
                date_modified, '%Y-%m-%d, %H:%M:%S')
        else:
            self.date_modified = datetime.now()
        self.title = title
        self.color = color
        self.details = details
        self.start_time = start_time
        self.end_time = end_time
        self.is_all_day = is_all_day
        self.is_recurrent = is_recurrent
        self.repetition_value = repetition_value
        self.repetition_type = repetition_type
        self.repetition_subtype = repetition_subtype

    '''
    short()
        short form representation of the Task model
    '''

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'color': self.color,
            'start_time': self.start_time.strftime("%Y-%m-%d, %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d, %H:%M:%S")
        }

    '''
    long()
        long form representation of the Task model
    '''

    def long(self):
        return {
            'id': self.id,
            'date_created': self.date_created.strftime("%Y-%m-%d, %H:%M:%S"),
            'date_modified': self.date_modified.strftime("%Y-%m-%d, %H:%M:%S"),
            'calendar_id': self.calendar_id,
            'title': self.title,
            'color': self.color,
            'details': self.details,
            'start_time': self.start_time.strftime("%Y-%m-%d, %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d, %H:%M:%S"),
            'is_all_day': self.is_all_day,
            'is_recurrent': self.is_recurrent,
            'repetition_value': self.repetition_value,
            'repetition_type': self.repetition_type,
            'repetition_subtype': self.repetition_subtype
        }

    def __repr__(self):
        return json.dumps(self.long())

    @staticmethod
    def _add_task_to_task_list(
        tasks_list,
        day,
        month,
        task,
        view_past_tasks=True
    ):
        if not view_past_tasks:
            # Check if this task should be hidden
            start_time = datetime.now()
            task_end_time = datetime(
                start_time.year,
                month,
                day,
                task.end_time.hour,
                task.end_time.minute,
                task.end_time.second)
            if task_end_time < start_time:
                return
        if month not in tasks_list:
            tasks_list[month] = {}
        if day not in tasks_list[month]:
            tasks_list[month][day] = []
        tasks_list[month][day].append(task.long())

    @staticmethod
    def getTasks(calendar_id, year, month, view_past_tasks):
        tasks = []
        if view_past_tasks:
            m, y = Calendar.previous_month_and_year(year, month)
            start_time = datetime(y, m, 24)
        else:
            start_time = datetime.now()
        m, y = Calendar.next_month_and_year(year, month)
        end_time = datetime(y, m, 6)

        # Query and add non recurrent tasks
        tasks_query = Task.query.join(Calendar).filter(
            Task.calendar_id == calendar_id).filter(
            not Task.is_recurrent,
            Task.end_time >= start_time,
            Task.start_time < end_time
        ).all()
        for task in tasks_query:
            tasks.append(task.long())

        # Query and add recurrent tasks
        recurrent_tasks_query = Task.query.join(Calendar).filter(
            Task.calendar_id == calendar_id).filter(
            Task.is_recurrent,
            extract('year', Task.start_time) == end_time.year,
            extract('month', Task.start_time) <= end_time.month
        ).all()
        for task in recurrent_tasks_query:
            tasks.append(task.long())

        return tasks

    @staticmethod
    def getTask(task_id):
        return Task.query.get(task_id)

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        db.session.commit()


Calendar.tasks = relationship(
    "Task", order_by=Task.id, cascade="all, delete", back_populates="calendar")
