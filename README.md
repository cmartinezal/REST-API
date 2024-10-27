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

A REST API is an interface that two computer systems use to exchange information securely over the internet. Most business applications have to communicate with other internal and third-party applications to perform various tasks. Some examples include:

- Social media sites like Twitter, Facebook use REST APIs to integrate with third-party applications and allow posting updates
- Ridesharing apps like Uber and Lyft use REST APIs to coordinate cars, obtain maps, fares and location data
- Video, music streaming through Netflix, Spotify use REST APIs to get info on media files from servers

### RESTful service

A RESTful service is a web service that follows the Representational State Transfer (REST) architectural style. RESTful services are designed to work well on the web and are built on the HTTP protocol. They use a client/server architecture and a standardized interface and protocol to exchange resource representations between clients and servers.

RESTful services often use a consistent set of HTTP methods (e.g., GET, POST, PUT, DELETE) to manage resources.

- `GET` retrieves data
- `POST` creates data
- `PUT` updates data
- `DELETE` removes data

For example, if a REST API manages a database of superheroes, a GET request to `/superheroes` could retrieve a list of all superheroes, while a POST request to `/superheroes` could add a new superhero to the database.

### JWT Authentication

JWT, or JSON Web Token, is a compact, URL-safe means of representing claims to be transferred between two parties in a secure way. For APIs, JWTs are commonly used as authorization tokens to verify the identity of users and control access to secured resources.

- When a user logs in, they provide valid credentials, which are verified by the API
- Once authenticated, the server generates a JWT containing user-specific claims (like user ID, roles, and expiration time) and signs it with a secret key
- For subsequent requests, the client sends the JWT in the Authorization header, usually prefixed with Bearer, like so: `Authorization: Bearer <token>`
- The server verifies the token using the secret key or a public key if asymmetric encryption is used. If valid, the user is granted access; otherwise, the request is denied
  
#### Example JWT Structure

A JWT has three parts:

1. **Header**: Specifies the algorithm and token type (usually HS256 and JWT)
2. **Payload**: Contains the claims (e.g., user data)
3. **Signature**: Validates the token’s integrity

Each part is base64-encoded and concatenated, separated by dots (.).

## Project Architecture

REST APIs use a client-server model to design networked applications, separating the user interface (client) from the back-end services (server). The client and server are independent of each other, and their interactions are limited to the client sending a request to the server, and the server responding. This separation of concerns makes user interfaces very portable and server elements more scalable.

This project uses a client-server architecture with requests managed through HTTP. It has been implemented in Python using the Flask framework, with API documentation provided through Swagger.

<br/>

![API architecture](https://github.com/user-attachments/assets/f2d27668-95ec-40f2-b488-e22f6a0824ce)

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

## Project Files

- **README.md**: Contains the project description along with installation and execution instructions
- **Pipfile**: File to specify all required dependencies to install the project using pipenv command
- **Pipfile.lock**: Is intended to specify, based on the packages present in Pipfile, which specific version of those should be used, avoiding the risks of automatically upgrading packages that depend upon each other and breaking your project dependency tree
- **LICENSE**: MIT license that describe the legal terms and conditions for using, distributing, and modifying the software
- **.pylintrc**: Configuration file to use pylint as a code analysis tool or linter program during the project development
- **src/superheroes.db**: Database file created using SQLite3. Allows users to connect to the database and query the existing data used for the API
- **src/app.py**: Main entry point for this Flask application. It initializes the web application, sets up routes (URLs), the JWT configuration and defines how the application should behave
- **static/swagger.json**: It includes the Swagger definition in JSON format that describes the structure of the REST API and builds the interactive documentation. It is based on the OpenAPI Specification version 3
- **src/routes/utils/\_\_init\_\_.py**: Module that inits utils package
- **src/routes/utils/database.py**: Module contained in utils package to manage the interactions with the data layer contained in the SQLite3 database
- **src/routes/utils/validations.py**: Module contained in utils package to validate body payloads in the API requests
- **src/routes/v1/auth/\_\_init\_\_.py**: Module contained in auth package that defines the authentication routes for the API version 1
- **src/routes/v1/auth/helpers.py**: Module contained in auth package that manages the logic for authentication routes for the API version 1
- **src/routes/v1/superheroes/\_\_init\_\_.py**: Module contained in auth package that defines the superheroes routes for the API version 1
- **src/routes/v1/superheroes/helpers.py**: Module contained in auth package that manages the logic for superheroes routes for the API version 1
- **src/routes/v1/superpowers/\_\_init\_\_.py**: Module contained in auth package that defines the superpowers routes for the API version 1
- **src/routes/v1/superpowers/helpers.py**: Module contained in auth package that manages the logic for superpowers routes for the API version 1
- **src/routes/v1/users/\_\_init\_\_.py**: Module contained in auth package that defines the users routes for the API version 1
- **src/routes/v1/users/helpers.py**: Module contained in auth package that manages the logic for users routes for the API version 1

## Getting Started

### Prerequisites

Python 3 must be installed. Check your version with:

```sh
python3 --version
```

### Installation

pipenv must be installed. You can install it with the following command:

```sh
pip install pipenv --user
```

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

Swagger is based on the OpenAPI Specification (OAS), a format for defining RESTful API endpoints, their HTTP methods, parameters, request and response formats, and authentication requirements.
Written in JSON or YAML, an OpenAPI document acts as a blueprint of the API that describes every aspect, including data types and validation rules.

![Screenshot 2024-10-26 at 19 54 29](https://github.com/user-attachments/assets/1ffbcfa7-a81b-41fc-8288-3f27ce08fe19)

- Swagger Web: ```http://127.0.0.1:5000/api/docs```

- JSON: ```http://127.0.0.1:5000/static/swagger.json```

### Authentication Endpoints

The authentication is based in JSON Web Token (JWT)\
The auth token is required to access to users secured endpoints.\
The refresh token endpoint exists to enable authorization servers to use short lifetimes for access tokens without needing to involve the user when the token expires.

![image](https://github.com/user-attachments/assets/c92f1099-a025-41ea-922a-d5395c9755dd)

The requests can be performed to the following urls:

- **POST** ```http://127.0.0.1:5000/api/v1/auth/token```
- **POST** ```http://127.0.0.1:5000/api/v1/auth/refresh```

### REST API Endpoints

![Screenshot 2024-10-26 at 20 08 26](https://github.com/user-attachments/assets/b7aeaff7-d539-4096-95a7-9434a981539f)

There are three groups of endpoints grouped by entity, Users, Superheroes and Superpowers.

- **Users:** Manages the users that have access to to the secured API endpoints
- **Superheroes:** Manages the superheroes and their assigned superpowers
- **Superpowers:** Manages the superpowers that will be assigned to the superheroes

## Example: Get all superheroes

### 1. Get token with user data

Use endpoint POST api/v1/auth/token.
You can use this test user to authorize:

- email: ```hamish.schmidt@web.com```
- password: ```secret```
  
A JWT will be issued for the test user specified:

![image](https://github.com/user-attachments/assets/9a73f47d-91a9-432c-98ae-2679edb76362)

Copy the value of access_token in Authorization to allow Swagger to send the Authorization header required in the secured endpoints:

![image](https://github.com/user-attachments/assets/c3164804-8473-4102-a871-9c3a4e197986)

### 2. Access to Get all superheroes secured endpoint

As we can see the authorization header is sent in the request and we can access to the secured endpoint and obtain the list of superheroes in the response body:

![image](https://github.com/user-attachments/assets/d94a0f79-c58a-4df6-8475-346e0c642a2c)
