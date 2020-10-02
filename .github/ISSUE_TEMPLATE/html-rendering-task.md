---
name: Html rendering and display task
about: Defining how the contents of each webpage is rendered using Django HTML templates, including the rendering of dynamic data received from the database.
title: "[ISSUE TITLE]"
labels: html rendering
assignees: ''

---

## Before you begin:
Make sure you understand how Django templates work:
  - https://docs.djangoproject.com/en/3.1/topics/templates/.
  - https://docs.djangoproject.com/en/3.1/ref/templates/language/
  - https://docs.djangoproject.com/en/3.1/ref/templates/builtins/
  
If the issue involves user input forms, also read up on Django forms:
  - https://docs.djangoproject.com/en/3.1/topics/forms/
  - https://docs.djangoproject.com/en/3.1/ref/forms/fields/

## App folder
This issue pertains to the files contained in the website app folder: 
- `scope_2gzm/INSERT_APPNAME`. 

## Tasks for `forms.py`:
NOTE: Forms are only needed if the user is expected to input some information and send it back to be stored in the website database. 
EXAMPLE: 
- [ ] Create class `ExampleForm`
  - [ ] Required information about the form input fields
  - [ ] ...

## Template context variables:
- `EXAMPLE_VAR_1` (type: TYPE)
  DESCRIPTION OF VARIABLE...
- `EXAMPLE_VAR_2` (type: TYPE)
  DESCRIPTION OF VARIABLE...

## Tasks for template html file(s):
EXAMPLE:
- [ ] Create file `templates/APP/PAGE_NAME.html`
  - [ ] Required page element 1.
  - [ ] Required page element 2.
  - [ ] ...

## Example outputs:

### `PAGE_NAME.html`
```
{% extends "templates/base.html" %}
{% load static %}

{% block page_content %}

PAGE CONTENT GOES HERE

{% endblock %}
```
