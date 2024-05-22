from flask import Flask, render_template, request, jsonify, redirect
# from blueprints.basic_endpoints import blueprint as basic_endpoints
# from blueprints.jinja_endpoint import blueprint as jinja_template_blueprint
# from blueprints.documented_endpoints import blueprint as documented_endpoint
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import json
# Import for Migrations
from flask_migrate import Migrate, migrate

app = Flask(__name__)

# api = Api(app, title="My test api", doc='/')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['RESTPLUS_MASK_SWAGGER'] = False
# app.register_blueprint(basic_endpoints)
# app.register_blueprint(jinja_template_blueprint)
# app.register_blueprint(documented_endpoint)
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)

# Define a sample resource
class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello, World!'})

# Models
# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Define a resource to return a list of users
class Users(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(user_list)


# Models
class Profile(db.Model):
    # Id : Field which stores unique id for every row in 
    # database table.
    # first_name: Used to store the first name if the user
    # last_name: Used to store last name of the user
    # Age: Used to store the age of the user
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"


class CompanyValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(2000), unique=False, nullable=False)
    icon_id = db.Column(db.Integer, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Title : {self.title}, description: {self.description}"
# Add the resources to the API
# api.add_resource(HelloWorld, '/')
# api.add_resource(Users, '/users')

# Configure Swagger UI
SWAGGER_URL = '/api/swagger'
# API_URL = '/swagger.json'
API_URL = '/swaggeryy'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))
    
    
# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    return f'Hello, {name}!'

# @app.route('/basic_api/hello_world')
# def hello_world():
#     return 'Hello, World!'


@app.route('/basic_api/entities', methods=['GET', 'POST'])
def entities():
    if request.method == "GET":
        return {
            'message': 'This endpoint should return a list of entities',
            'method': request.method
        }
    if request.method == "POST":
        return {
            'message': 'This endpoint should create an entity',
            'method': request.method,
		'body': request.json
        }

@app.route('/basic_api/entities/<int:entity_id>', methods=['GET', 'PUT', 'DELETE'])
def entity(entity_id):
    if request.method == "GET":
        return {
            'id': entity_id,
            'message': 'This endpoint should return the entity {} details'.format(entity_id),
            'method': request.method
        }
    if request.method == "PUT":
        return {
            'id': entity_id,
            'message': 'This endpoint should update the entity {}'.format(entity_id),
            'method': request.method,
		'body': request.json
        }
    if request.method == "DELETE":
        return {
            'id': entity_id,
            'message': 'This endpoint should delete the entity {}'.format(entity_id),
            'method': request.method
        }


@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)

@app.route('/')
def index():
      # Query all data and then pass it to the template
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)


@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')


# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
    
    # In this function we will input data from the 
    # form page and store it in our database.
    # Remember that inside the get the name should
    # exactly be the same as that in the html
    # input fields
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")

    # create an object of the Profile class of models
    # and store data as a row in our datatable
    if first_name != '' and last_name != '' and age is not None:
        p = Profile(first_name=first_name, last_name=last_name, age=age)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unique id and 
    # redirects to home page
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')






@app.route('/values')
def values_index():
      # Query all data and then pass it to the template
    list = CompanyValue.query.all()
    return render_template('values/index.html', values=list)

@app.route('/value/add')
def values_add():
    return render_template('values/add_value.html')

# function to add profiles
@app.route('/value/add', methods=["POST"])
def values_add_post():
    
    # In this function we will input data from the 
    # form page and store it in our database.
    # Remember that inside the get the name should
    # exactly be the same as that in the html
    # input fields
    title = request.form.get("title")
    description = request.form.get("description")
    icon_id = request.form.get("icon_id")

    # create an object of the Profile class of models
    # and store data as a row in our datatable
    if title != '' and description != '' and icon_id is not None:
        p = CompanyValue(title=title, description=description, icon_id=icon_id)
        db.session.add(p)
        db.session.commit()
        return redirect('/values')
    else:
        return redirect('/value/add')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)