# Django Old Records

A simple Django app with tools to manage old records of Django models

## Install

`pip install django-old-records`

Add `django_old_records` to your project's `INSTALLED_APPS`
## Usage

There is a manager that decides if a record is too old based on a date field (`created_at` by default) and a `max_age`. Ex.:

```python
from django_old_records import OldRecordsManager
from django.db import models

class Cat(models.Model):

    name = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

    max_age = 365 * 20 # 20 years

    old_records = OldRecordsManager()
```

```python
Cat.old_records.all() # lists all cat records older than 20 years
```

`max_age` could be an integer representing days or a python `timedelta` for a more detailed value. Ex.:

```python
from django_old_records import OldRecordsManager
from django.db import models
from datetime import timedelta

class Cat(models.Model):

    name = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

    max_age = timedelta(hours=4, seconds=20)

    old_records = OldRecordsManager()
```

```python
Cat.old_records.all() # lists all cat records older than 4 hours and 20 seconds
```

If your model's `created_at` has a different name you can specify it with the `created_at_field` attribute. Ex.:

```python
class Cat(models.Model):

    name = models.CharField()
    was_born = models.DateTimeField(auto_now_add=True)

    created_at_field = 'was_born'
    max_age = 365 * 20 # 20 years

    old_records = OldRecordsManager()
```
There is also a management command that deletes all old records from all models:

`python manage.py delete_old_records`
