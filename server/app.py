#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = [n.to_dict() for n in Plant.query.all()]

        response = make_response(jsonify(plants), 200)

        return response

    def post(self):
        new_plant = Plant()

        for key, value in request.json.items():
            setattr(new_plant, key, value)
            
        # or new_plant = Plant(**request.get_json())

        db.session.add(new_plant)
        db.session.commit()

        response = make_response(jsonify(new_plant.to_dict()), 201)

        return response


api.add_resource(Plants, '/plants')


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()

        response = make_response(jsonify(plant), 200)
        return response


api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
