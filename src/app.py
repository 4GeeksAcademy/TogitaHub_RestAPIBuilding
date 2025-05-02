"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Person, Vehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Simulación de un usuario logeado en el sistema
CURRENT_USER_ID = 1

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET', 'POST'])
def handle_people():
    if request.method == 'GET':
        people = db.session.execute(db.select(Person)).scalars().all()
        return jsonify([person.serialize() for person in people])
    elif request.method == 'POST':
        data = request.get_json()
        new_person = Person(
            name=data.get('name'),
            gender=data.get('gender'),
            homeworld_id=data.get('homeworld_id')
        )
        db.session.add(new_person)
        db.session.commit()
        return jsonify(new_person.serialize()), 201

@app.route('/people/<int:people_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_person(people_id):
    person = db.session.get(Person, people_id)
    if not person:
        return jsonify({"message": "Person not found"}), 404

    if request.method == 'GET':
        return jsonify(person.serialize())
    elif request.method == 'PUT':
        data = request.get_json()
        person.name = data.get('name', person.name)
        person.gender = data.get('gender', person.gender)
        person.homeworld_id = data.get('homeworld_id', person.homeworld_id)
        db.session.commit()
        return jsonify(person.serialize())
    elif request.method == 'DELETE':
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Person deleted"}), 200

@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():
    if request.method == 'GET':
        planets = db.session.execute(db.select(Planet)).scalars().all()
        return jsonify([planet.serialize() for planet in planets])
    elif request.method == 'POST':
        data = request.get_json()
        new_planet = Planet(
            name=data.get('name'),
            climate=data.get('climate'),
            terrain=data.get('terrain'),
            population=data.get('population')
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201


@app.route('/planets/<int:planet_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_planet(planet_id):
    planet = db.session.get(Planet, planet_id)
    if not planet:
        return jsonify({"message": "Planet not found"}), 404

    if request.method == 'GET':
        return jsonify(planet.serialize())
    elif request.method == 'PUT':
        data = request.get_json()
        planet.name = data.get('name', planet.name)
        planet.climate = data.get('climate', planet.climate)
        planet.terrain = data.get('terrain', planet.terrain)
        planet.population = data.get('population', planet.population)
        db.session.commit()
        return jsonify(planet.serialize())
    elif request.method == 'DELETE':
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planet deleted"}), 200

@app.route('/vehicles', methods=['GET', 'POST'])
def handle_vehicles():
    if request.method == 'GET':
        vehicles = db.session.execute(db.select(Vehicle)).scalars().all()
        return jsonify([vehicle.serialize() for vehicle in vehicles])
    elif request.method == 'POST':
        data = request.get_json()
        new_vehicle = Vehicle(
            name=data.get('name'),
            model=data.get('model'),
            manufacturer=data.get('manufacturer'),
            crew=data.get('crew'),
            passengers=data.get('passengers')
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify(new_vehicle.serialize()), 201


@app.route('/vehicles/<int:vehicle_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_vehicle(vehicle_id):
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    if request.method == 'GET':
        return jsonify(vehicle.serialize())
    elif request.method == 'PUT':
        data = request.get_json()
        vehicle.name = data.get('name', vehicle.name)
        vehicle.model = data.get('model', vehicle.model)
        vehicle.manufacturer = data.get('manufacturer', vehicle.manufacturer)
        vehicle.crew = data.get('crew', vehicle.crew)
        vehicle.passengers = data.get('passengers', vehicle.passengers)
        db.session.commit()
        return jsonify(vehicle.serialize())
    elif request.method == 'DELETE':
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({"message": "Vehicle deleted"}), 200

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = db.session.execute(db.select(User)).scalars().all()
        return jsonify([user.serialize() for user in users])
    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            # ¡Recuerda hashear la contraseña en producción!
            password=data.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if request.method == 'GET':
        return jsonify(user.serialize())
    elif request.method == 'PUT':
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        # ¡Considera cómo manejar esto de forma segura!
        user.password = data.get('password', user.password)
        db.session.commit()
        return jsonify(user.serialize())
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = db.session.get(User, CURRENT_USER_ID)
    if user:
        favorite_planets = [planet.serialize()
                            for planet in user.favorite_planets]
        favorite_people = [person.serialize()
                           for person in user.favorite_people]
        favorite_vehicles = [vehicle.serialize()
                             for vehicle in user.favorite_vehicles]
        return jsonify({"planets": favorite_planets, "people": favorite_people, "vehicles": favorite_vehicles})
    return jsonify({"message": "User not found"}), 404

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def handle_favorite_planet(planet_id):
    user = db.session.get(User, CURRENT_USER_ID)
    planet = db.session.get(Planet, planet_id)
    if not user or not planet:
        return jsonify({"message": "User or planet not found"}), 404

    if request.method == 'POST':
        if planet not in user.favorite_planets:
            user.favorite_planets.append(planet)
            db.session.commit()
            return jsonify({"message": f"Planet '{planet.name}' added to favorites"}), 201
        return jsonify({"message": f"Planet '{planet.name}' is already in favorites"}), 200
    elif request.method == 'DELETE':
        if planet in user.favorite_planets:
            user.favorite_planets.remove(planet)
            db.session.commit()
            return jsonify({"message": f"Planet '{planet.name}' removed from favorites"}), 200
        return jsonify({"message": f"Planet '{planet.name}' is not in favorites"}), 404

@app.route('/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def handle_favorite_person(people_id):
    user = db.session.get(User, CURRENT_USER_ID)
    person = db.session.get(Person, people_id)
    if not user or not person:
        return jsonify({"message": "User or person not found"}), 404

    if request.method == 'POST':
        if person not in user.favorite_people:
            user.favorite_people.append(person)
            db.session.commit()
            return jsonify({"message": f"Person '{person.name}' added to favorites"}), 201
        return jsonify({"message": f"Person '{person.name}' is already in favorites"}), 200
    elif request.method == 'DELETE':
        if person in user.favorite_people:
            user.favorite_people.remove(person)
            db.session.commit()
            return jsonify({"message": f"Person '{person.name}' removed from favorites"}), 200
        return jsonify({"message": f"Person '{person.name}' is not in favorites"}), 404

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST', 'DELETE'])
def handle_favorite_vehicle(vehicle_id):
    user = db.session.get(User, CURRENT_USER_ID)
    vehicle = db.session.get(Vehicle, vehicle_id)
    if not user or not vehicle:
        return jsonify({"message": "User or vehicle not found"}), 404

    if request.method == 'POST':
        if vehicle not in user.favorite_vehicles:
            user.favorite_vehicles.append(vehicle)
            db.session.commit()
            return jsonify({"message": f"Vehicle '{vehicle.name}' added to favorites"}), 201
        return jsonify({"message": f"Vehicle '{vehicle.name}' is already in favorites"}), 200
    elif request.method == 'DELETE':
        if vehicle in user.favorite_vehicles:
            user.favorite_vehicles.remove(vehicle)
            db.session.commit()
            return jsonify({"message": f"Vehicle '{vehicle.name}' removed from favorites"}), 200
        return jsonify({"message": f"Vehicle '{vehicle.name}' is not in favorites"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
