# Chop Shop API

A REST API for a mechanic shop built with Flask and MySQL. Handles customers, mechanics, service tickets, and inventory.

## Tech

- Flask
- SQLAlchemy
- Marshmallow
- Flask-Limiter
- Flask-Caching
- flask-swagger-ui
- python-jose
- MySQL
- python-dotenv

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Create a .env file in the root: SQLALCHEMY_DATABASE_URI=mysql+mysqlconnector://root:<your_password_here>@localhost/chop_shop
4. Create the chop_shop database in MySQL
5. Run it
6. API documentation available at http://127.0.0.1:5000/api/docs

## Endpoints

### Customers

- POST /customers/ - Create a customer
- POST /customers/login - Login and get a token
- GET /customers/ - Get all customers (paginated)
- GET /customers/my-tickets - Get your service tickets (requires token)
- PUT /customers/<id> - Update a customer (requires token)
- DELETE /customers/<id> - Delete a customer (requires token)

### Mechanics

- POST /mechanics/ - Add a mechanic
- GET /mechanics/ - Get all mechanics sorted by tickets worked
- PUT /mechanics/<id> - Update a mechanic
- DELETE /mechanics/<id> - Delete a mechanic

### Service Tickets

- POST /service-tickets/ - Create a ticket
- GET /service-tickets/ - Get all tickets
- GET /service-tickets/<id> - Get a specific ticket
- PUT /service-tickets/<ticket_id>/edit - Add or remove mechanics from a ticket
- PUT /service-tickets/<ticket_id>/add-part/<inventory_id> - Add a part to a ticket

### Inventory

- POST /inventory/ - Add a part
- GET /inventory/ - Get all parts
- GET /inventory/<id> - Get a specific part
- PUT /inventory/<id> - Update a part
- DELETE /inventory/<id> - Delete a part

## Status Codes

200 - OK, request worked
201 - Created, new record was added
400 - Bad request, something wrong with the data you sent. Check your JSON for missing fields or typos
404 - Not found, the id you used doesnt exist in the database
405 - Method not allowed, that route doesnt support that HTTP method
500 - Server error, something broke on the backend
