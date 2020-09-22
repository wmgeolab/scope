---
name: Data models and schemas task
about: Defining the data models (i.e. database tables) needed for the website.
title: "[ISSUE TITLE]"
labels: data model config
assignees: ''

---

## Description
Short description of what to do in this task. 

## Before you begin:
Make sure you understand how Django models and fields work:
  - https://docs.djangoproject.com/en/3.1/topics/db/models/
  - https://docs.djangoproject.com/en/3.1/ref/models/fields/
  
Be aware of how to link models:
  - https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_one/
  - https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/

## App folder
This issue pertains to the files contained in the website app folder: 
- `scope_2gzm/INSERT_APPNAME`. 

## Tasks for `models.py`:
EXAMPLE: 
- [ ] Create model class `ModelClassName`:
  - [ ] Field 1...
  - [ ] Field 2...
  - [ ] ...

## Tasks if a model has been altered:
NOTE: Only include this section if an existing model has been altered (model renamed, or fields renamed, dropped, or changed):
- [ ] Find and update all references to the altered model **across all** website apps `views.py` files.
- [ ] Find and update all models that link to the altered model **across all** website apps `models.py` files.

## Tasks to sync changes to the database
Example:
- [ ] In the commandline, do `python manage.py makemigrations`
- [ ] Then `python manage.py migrate`

