# Customers REST API

## Getting Started
## Authorization

The API uses Basic Auth.

## Actions
- [Get All Customers](#get-all-customers)
- [Create New Customer](#create-new-customer)
- [Edit A Customer](#edit-a-customer)
- [Delete A Customer](#delete-a-customer)

### Get All Customers

Retrieves all customers in the database.

`Endpoint`: GET /users/api/v1.0/users

#### Request
`Content-Type`: application/json
##### Query Parameters
| Name | Data Type | Required/ Optional | Description |
| --- | --- | --- | --- |
| `sort-by` | string | optional | The attribute of the customer that we want to sort by Currently, only `dob` is accepted. When `sort_by`=`dob`, we return a list of customers sorted by date of birth starting from the most recent
| `number` | number | optional | When `sort-by` is specified, indicates the number of customers to be returned.

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
#### Request
`Content-Type`: application/json
##### Path Parameters
| Name | Data Type | Required/ Optional | Description |
| --- | --- | --- | --- |
| `user_id` | number | required | The id of the customer whose details will be edited