# REST-API
REST API built with Flask and documented with Swagger

## Prerequisites

Python 3 must be installed. Check your version with:

```sh
python3 --version
```

### Installation

To activate pipenv virtual environment and install all required libraries from Pipfile use this commands:

```sh
pipenv shell
pipenv install
```

### Run the project

Define the Flask environment variables and access the application in the url http://127.0.0.1:5000

```sh
export FLASK_APP=app.py
export FLASK_ENV=production
flask run
```
