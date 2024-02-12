# Django shop catalog

This repository contains a simple Django app which is capable of
loading a json data and retrieving the loaded data. The data come in
a following format:

````
[
  {
    "ModelA": {
      "field1": "data",
      "field2": ["data", "array"]
    }
  },
  {
    "ModelB": {
      "field1": "data",
    }
  },
  {
    "ModelB": {
      "field1": "data",
    }
  }
]
````

Sample data are provided in file test_data.json.

## Installation
Clone the repository to your computer:

`git glone https://github.com/rastislavpapco/django-shop-catalog.git`

Create virtual environment for python.

`cd django-shop-catalog`

`python -m venv venv`

`source venv/Scripts/activate`

Install requirements.txt

`pip install -r requirements.txt`

## Running the app
Propagate model changes to database schema.

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py migrate --run-syncdb`

Run the app. The app runs on http://127.0.0.1:8000/ by default.

`python manage.py runserver`

## Endpoints
See swagger documentation on http://127.0.0.1:8000/docs/ . There are three endpoints:
* /catalog/upload/ - Upload catalog items to database.
 Accepts JSON body described on top of this page.
* /catalog/{model_type}/ - Get list of all model instances.
* /catalog/{model_type}/{model_id}/ - Get specific model instance.
