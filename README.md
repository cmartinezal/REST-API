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
        <li><a href="#run-project">Run the project</a></li>
      </ul>
    </li>
    <!-- <li><a href="#usage">Usage</a>
       <ul>
          <li><a href="#swagger-documentation">Swagger Documentation</a></li>
          <li><a href="#authorization-endpoints">Authorization Endpoints</a></li>
          <li><a href="#rest-api-endpoints">REST API Endpoints</a></li>
       </ul>
    <li>
        <a href="#example-get-all-users">Example: Get all users</a>
        <ul>
          <li><a href="#1-get-token-with-user-data">1. Get token with user data</a></li>
          <li><a href="#2-access-to-get-all-users-secured-endpoint">2. Access to Get all users secured endpoint</a></li>
       </ul>
    </li> -->
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

![rest api](https://github.com/user-attachments/assets/ab1b6842-a650-4649-949d-07a05d96a43f)


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
