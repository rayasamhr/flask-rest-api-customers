from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from functools import wraps
from dotenv import load_dotenv
import datetime
import uuid
import jwt
import os

app = Flask(__name__)

# Secret key will change every time we re-run the app
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Administrator(db.Model):
  id =  db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(50), unique=True)
  username = db.Column(db.String, unique=True)
  password = db.Column(db.String, nullable=False)

class Customer(db.Model):
  __tablename__ = 'customers'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  dob = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

  def __repr__(self):
      return f"<Customer {self.name}>"

# TODO: use abort here with missing token and invalid token messages
def check_for_token(func):
  @wraps(func)
  def wrapped(*args, **kwargs):
    token = None
    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    if not token:
      abort(403)
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
      admin = Administrator.query.filter_by(public_id=data['public_id']).first()
    except:
      abort(403)
    return func(admin, *args, **kwargs)
  return wrapped

@app.route('/')
def index():
  return 'Hello World'

# Create an admin account
@app.route('/admin', methods=['POST'])
def create_admin():
  if not request.json:
    abort(400)
  data = request.get_json()
  hashed_password = generate_password_hash(data['password'], method='sha256')
  new_admin = Administrator(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password)
  db.session.add(new_admin)
  db.session.commit()
  return jsonify({'message': 'Admin created'}), 200

# Verify an admin account
@app.route('/login')
def login():
  auth = request.authorization
  if auth and auth.username and auth.password:
    admin = Administrator.query.filter_by(username=auth.username).first()
    if admin and check_password_hash(admin.password, auth.password):
      token = jwt.encode({
      'public_id': admin.public_id, 
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)},
      app.config['SECRET_KEY'])
      return jsonify({'token': token})
  abort(401)

# Get all users
@app.route('/users/api/v1.0/users', methods=['GET'])
@check_for_token
def get_users(current_user):
  sort_by = request.args.get('sort_by', None)
  num = request.args.get('number', None)
  if (sort_by == 'dob'):
    customers = Customer.query.order_by(Customer.dob.desc()).limit(num).all()
  else:
    customers = Customer.query.all()
  results = [get_message(customer) for customer in customers]
  return jsonify({'customers': results}), 200
  
# TODO: decorate
# Get a single user
@app.route('/users/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
  user = Customer.query.get_or_404(user_id)
  return jsonify({'customer': get_message(user)}), 200

# Add a single user
@app.route('/users/api/v1.0/users', methods=['POST'])
@check_for_token
def create_user(current_user):
  if not request.json:
    abort(400)
  data = request.get_json()
  new_customer = Customer(name=data['name'], dob=data['dob'])
  db.session.add(new_customer)
  db.session.commit()
  return jsonify({'customer': get_message(new_customer)}), 201
# TODO: decorate

# Delete a single user
@app.route('/users/api/v1.0/users/<int:user_id>', methods=['DELETE'])
@check_for_token
def delete_user(current_user, user_id):
  user = Customer.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  return jsonify({'result': True}), 200

# Update a single user
@app.route('/users/api/v1.0/users/<int:user_id>', methods=['PUT'])
@check_for_token
def update_user(current_user, user_id):
  user = Customer.query.get_or_404(user_id)
  data = request.get_json()
  user.name = data['name']
  user.dob = data['dob']
  user.updated_at = db.func.now()
  db.session.add(user)
  db.session.commit()
  return jsonify({'customer': get_message(user)}), 200

def get_message(user):
  return {
    'id': user.id,
    'name': user.name,
    'dob': user.dob,
    'updated_at': user.updated_at
  }

# TODO: Check if this error is formatted properly
@app.errorhandler(401)
def unauthorised(error):
  return make_response(jsonify({'error': 'Could not verify'}), 401, {
    'WWW-Authenticate': 'Basic realm="Login required!"'
  })

@app.errorhandler(403)
def forbidden(error):
  return make_response(jsonify({'error': 'Forbidden'}), 403)

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
  app.run()