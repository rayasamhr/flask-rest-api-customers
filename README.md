# Customers REST API
## Contents
1. [Getting Started](#getting-started)
2. [Authorization](#authorization)
3. [Actions](#actions)

## Getting Started

Requirements: 
- Python, pip
- PostgreSQL
- Virtualenv

Setup:
1. In a terminal/ command line window, navigate to the root folder of the project
1. Create a virtual environment `env` by running:
    - [Mac/Linux] `python3 -m venv env`
    - [Windows] `py -m venv env`
1. Activate the virtual environment by running:
    - [Max/Linux] `source env/bin/activate`
    - [Windows] `.\env\Scripts\activate`
1. To install required dependencies, run `pip install -r requirements.txt`
1. Using psql, create the `customers` database by entering `create database customers;`
1. In the root folder of the project, create a file named `.env` with the following contents. Substitute {username} and {password} with the username and password of the Postgres user who owns the `customers` database
    ```
    FLASK_ENV=development
    SQLALCHEMY_DATABASE_URI='postgresql://{username}:{password}@localhost:5432/customers'
    ```
1. Start the PostgreSQL service
1. On the terminal/ command line window, create the required tables by running the following:
    ```
    flask db init
    flask db migrate
    flask db upgrade
    ```
1. To start the app, run `flask start`
## Authorization

1. [Create An Administrator Account](#create-an-administrator-account)
2. [Generate Token](#generate-token)
3. [Use Token](#use-token)

In this example, for demonstration purposes, we provide an unsecured method to create an administrator account. Using an administrator username and password, you are able to generate a JWT token allowing you to access the [Customer resource endpoints](#actions). 

### Create an Administrator Account
`Endpoint`: POST /admin

#### Request
`Content-Type`: application/json

##### Path Properties

| Name | Data Type | Required/ Optional |
| --- | --- | --- |
| `username` | string | required |
| `password` | string | required |

### Generate Token
`Endpoint`: /login

The API uses Basic Auth. To login, encode a valid administrator username and password (created [above](#create-an-administrator-account)) with base64:

```
 echo -n {username}:{password} | base64
```
This will return a base64-encoded string.

Example usage: `echo -n Admin:1234 | base64` produces an output `QWRtaW46MTIzNA==`

#### Request

`Authorization`: `Basic {str}` where `{str}` is the base64-encoded string output 

Example usage: `Authorization`: `Basic QWRtaW46MTIzNA==`

#### Response

| Name | Data Type | Description |
| --- | --- | --- |
| `jwt-token` | string | Token required to access customer resource endpoints |

### Use Token

The token expires within 2 minutes.

The token should be passed into the `x-access-token` header field of the following requests.

## Actions
1. [Get All Customers](#get-all-customers)
1. [Create New Customer](#create-new-customer)
1. [Edit A Customer](#edit-a-customer)
1. [Delete A Customer](#delete-a-customer)

### Get All Customers

Retrieves all customers in the database.

`Endpoint`: GET /users/api/v1.0/users

#### Request
`Content-Type`: application/json
##### Query Parameters
| Name | Data Type | Required/ Optional | Description |
| --- | --- | --- | --- |
| `sort_by` | string | optional | The attribute of the customer that we want to sort by. When `sort_by`=`dob`, we return a list of customers sorted by date of birth starting from the most recent.
| `number` | number | optional | When `sort_by` is specified, indicates the number of customers to be returned.

### Create New Customer

Adds a new customer to the database.

`Endpoint`: POST /users/api/v1.0/users

#### Request
`Content-Type`: application/json
##### Path Properties

| Name | Data Type | Required/ Optional | Description |
| --- | --- | --- | --- |
| `name` | string | required | The name of the customer
| `dob` | datetime | required | The birthdate of the customer in MM/DD/YYYY format

### Edit A Customer

Updates a specific customer in the database.

`Endpoint`: PUT /users/api/v1.0/users/{user_id}

#### Request
`Content-Type`: application/json
##### Path Parameters
| Name | Data Type | Required/ Optional | Description |
| --- | --- | --- | --- |
| `user_id` | number | required | The id of the customer whose details will be edited
##### Path Properties

| Name | Data Type | Required/ Optional | Description |
| --- | --- | --- | --- |
| `name` | string | required | The name of the customer
| `dob` | datetime | required | The birthdate of the customer in MM/DD/YYYY format

### Delete A Customer

`Endpoint`: DELETE /users/api/v1.0/users/{user_id}
#### Request
`Content-Type`: application/json
##### Path Parameters
| Name | Data Type | Required/ Optional | Description |
| --- | --- | --- | --- |
| `user_id` | number | required | The id of the customer whose details will be edited