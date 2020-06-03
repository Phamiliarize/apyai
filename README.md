# apyai

**a-p-yai**

A remarkably small and light-weight Python 3 boilerplate for quickly prototyping RESTful microservices. Built on Falcon and Peewee w/ postgresql.

## Installation
Create a Python 3 virtual environment and install required packages.

```
python -m venv venv
pip install -r requirements.txt
```

## Running the API
Once you have a running postgresql database running, go ahead and put in the credentials or information. For our sample, we will use peewee/peewee and manabi-dev as an homage to two things that brought us into creation. Otherwise, set this to whatever you want.

```
database = {
    "database": "manabi-dev",
    "user":"peewee",
    "password":"peewee",
    "host": "127.0.0.1",
    "port": 5432
}
```


Utilize Gunicorn to run the app during development.

```
gunicorn --reload app
```

## Building your REST API
apyai trys to keep things simple- and this knowingly removes some flexibility. This is fine and accepted as a trade-off for a very simple & reusable pattern. 


When designing an API:

1. All endpoints are defined and routed in via *app.py*
2. SingleApi endpoints should end in an id. ListApi endpoints should not.
3. ListAPI and SingleAPIs are not one in the same- define seperately.
4. Resources must have a model and a view- the views merely extend ListAPI or SingleAPI.
5. Resources use id as a primary key
6. Use language to your benefit

### Example
See the test resouce as an example: don't forget the on_method classes can be overrode in the view by redifining the fuction.
