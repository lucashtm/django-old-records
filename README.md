# Django Old Records

A simple Django app with tools to manage old records of Django models

## Install

`pip install django-old-records`

## Usage

There is a manager that decides if a record is too old based on a date field (`created_at` by default) and a `max_age`. Ex.:

```python
from django_old_records import OldRecordsManager
from django.db import models

class Cat(models.Model):

    name = models.CharField()

    max_age = 365 * 20 # 20 years

    old_records = OldRecordsManager()


```

```python
Cat.old_records.all() # lists all cats older than 20 years
```

`max_age` could be an integer representing days or a python `timedelta` for a more detailed values.

There is also a management command that deletes all old records

`python manage.py delete_old_records`
