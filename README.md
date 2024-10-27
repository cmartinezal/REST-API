# REST-API

REST API built with Flask and documented with Swagger

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#project-architecture">Project Architecture</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#run-the-project">Run the project</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
       <ul>
          <li><a href="#swagger-documentation">Swagger Documentation</a></li>
          <li><a href="#authentication-endpoints">Authentication Endpoints</a></li>
          <li><a href="#rest-api-endpoints">REST API Endpoints</a></li>
       </ul>
    <li>
        <a href="#example-get-all-superheroes">Example: Get all superheroes</a>
        <ul>
          <li><a href="#1-get-token-with-user-data">1. Get token with user data</a></li>
          <li><a href="#2-access-to-get-all-superheroes-secured-endpoint">2. Access to Get all superheroes secured endpoint</a></li>
       </ul>
    </li>
  </ol>
</details>

## About The Project

This project establishes a REST API with JWT (JSON Web Token) authentication to manage superheroes, superpowers, and users.

RESTful services often use a consistent set of HTTP methods (e.g., GET, POST, PUT, DELETE) to manage resources.

- GET retrieves data
- POST creates data
- PUT updates data
- DELETE removes data

For example, if a REST API manages a database of superheroes, a GET request to `/superheroes` could retrieve a list of all superheroes, while a POST request to `/superheroes` could add a new superhero to the database.

## Project Architecture

This project uses a client-server architecture with requests managed through HTTP. It has been implemented in Python using the Flask framework, with API documentation provided through Swagger.
<br/>

![API architecture](https://github.com/user-attachments/assets/ed822001-d4f0-4e71-9764-3980053c420e)


The database has been created using SQLite3 that is a lightweight, serverless, self-contained SQL database engine. Unlike traditional database management systems that require a server, SQLite is file-based, meaning the entire database is stored in a single file on disk. This design makes it easy to set up and use, as there’s no need for configuration, installation, or a dedicated database server to run it.

To access the database and perform your own queries use the following command:

``` sh
sqlite3 superheroes.db
```

You can see the existing tables and schemas with these commands:

``` sh
.tables
.schema
```
<br/>

![Screenshot 2024-10-26 at 18 20 43](https://github.com/user-attachments/assets/be15ea8b-c700-4891-8171-a9644abc7137)


## Getting Started

### Prerequisites

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

Define the Flask environment variables, run flask from src folder and access the application in the url <http://127.0.0.1:5000>
Swagger documentation is available on: <http://127.0.0.1:5000/api/docs>

```sh
cd src
export FLASK_APP=app.py
export FLASK_ENV=production
flask run
```
## Usage

### Swagger Documentation

![Screenshot 2024-10-26 at 19 54 29](https://github.com/user-attachments/assets/1ffbcfa7-a81b-41fc-8288-3f27ce08fe19)


- Swagger Web: ```http://127.0.0.1:5000/api/docs```

- JSON: ```http://127.0.0.1:5000/static/swagger.json```

### Authentication Endpoints

The authentication is based in JSON Web Token (JWT)\
The auth token is required to access to users secured enpoints.\
The refresh token endpint exists to enable authorization servers to use short lifetimes for access tokens without needing to involve the user when the token expires.

![image](https://github.com/user-attachments/assets/c92f1099-a025-41ea-922a-d5395c9755dd)


The requests can be performed to the following urls:

- *POST* ```http://127.0.0.1:5000/api/v1/auth/token```
- *POST* ```http://127.0.0.1:5000/api/v1/auth/refresh```

### REST API Endpoints

![Screenshot 2024-10-26 at 20 08 26](https://github.com/user-attachments/assets/b7aeaff7-d539-4096-95a7-9434a981539f)

There are three groups of enpoints grouped by entity, Users, Superheores and Superpowers.

- *Users* Manages users that have access to to the secured API endpoints
- *Superheores* Manages the superheroes and their assigned superpowers
- *Superpowers* Manages the superpowers that will be assigned to the superheroes

## Example: Get all superheroes

### 1. Get token with user data

Use endpoint POST api/v1/auth/token.
You can use this test user to authorize:

- email: ```hamish.schmidt@web.com```
- password: ```secret```
  
A JWT will be issued for the test user specified:

![image](https://github.com/user-attachments/assets/9a73f47d-91a9-432c-98ae-2679edb76362)


Copy the value of access_token in Authorization to allow Swagger to send the Authorization header required in the secured enpoints:

![image](https://github.com/user-attachments/assets/c3164804-8473-4102-a871-9c3a4e197986)


### 2. Access to Get all superheroes secured endpoint

As we can see the authorization header is sent in the request and we can access to the secure endpoint and we obtain a list of superheroes in the response body:

![image](https://github.com/user-attachments/assets/d94a0f79-c58a-4df6-8475-346e0c642a2c)


