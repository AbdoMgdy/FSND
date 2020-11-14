from logging import error
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():
    print('hello')
    drinks = Drink.query.all()

    return jsonify({
        "sucess": True,
        "drinks": [drinks.short() for drink in drinks]
    })


@requires_auth('get:drinks-detail')
@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    })


@requires_auth('post:drinks')
@app.route('/drinks', methods=['POST'])
def store_drinks():
    data = request.get_json()

    try:
        drink = Drink(
            title=data['title'],
            recipe=data['recipe']
        )
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(400)


@requires_auth('patch:drinks')
@app.route('/drinks/<id>', methods=['PUT'])
def update_drink(id):
    drink = Drink.query.get(id)

    if not drink:
        abort(404)
    data = request.get_json()
    try:
        drink.title = data['title']
        drink.recipe = data['recipe']
        drink.update()
    except:
        abort(400)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


@requires_auth('delete:drinks')
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drinks(id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        drink.delete()
    except:
        abort(500)


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'unathorized'
    }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": 'resource not found'
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'bad request'
    }), 400


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'internal server error'
    }), 500
