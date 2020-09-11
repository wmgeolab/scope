## Before you begin:
Make sure you understand how Django templates work:
  - [ ] https://docs.djangoproject.com/en/3.1/topics/templates/.
  - [ ] https://docs.djangoproject.com/en/3.1/ref/templates/language/

## Template input variables:
- `EXAMPLE_VAR_1` (type: TYPE)
  DESCRIPTION OF VARIABLE...
- `EXAMPLE_VAR_2` (type: TYPE)
  DESCRIPTION OF VARIABLE...

## Tasks for `forms.py`:
Forms are only needed if the user is expected to input some information and send it back to be stored in the website database. 
EXAMPLE: 
- [ ] Create class `ExampleForm`
  - [ ] Required fields and types. 
    - [ ] CharField
  - [ ] ...

## Tasks for `views.py`:
EXAMPLE:
- [ ] Create file `templates/parsing/landing.html`
  - [ ] Conditional link button. 
    - [ ] If `has_checkout` == True
      - Go to checked out event (url name = 'event_continue')
    - [ ] Else
      - Go to event selection list (url name = 'event_new')

## Example outputs:

### `landing.html`
```
{% extends "templates/base.html" %}
{% load static %}

{% block page_content %}


<div style="width:100%">

{% if has_checkout %}
  <a class="btn" href="{% url 'event_continue' %}">
   Continue
  </a>
{% else %}
  <a class="btn" href="{% url 'event_new' %}">
   Start New
  </a>
{% endif %}

</div>


{% endblock %}
```
