from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from db import Product, SalesPoint, DeliveryRoute, DeliverySchedule, Inventory
from flasgger import Swagger
from flask_sqlalchemy  import SQLAlchemy
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soliuz.db'

DB = SQLAlchemy(app)

swagger = Swagger(app)

# ######## PRODUCTS ########### #
@app.route('/products', methods=['GET', 'POST'])
def products():
    # render all
    if request == 'GET':
        products = DB.session.query(Product).all()
        product_list = []
        for product in products:
            product_dict = {
                'id': product.id,
                'name': product.name,
                'expiry_date': product.expiry_date,
                'volume': product.volume,
                'weight': product.weight
            }
            product_list.append(product_dict)
        return jsonify(product_list)
    # create
    if request == 'POST':
        product = request.get_json()
        new_product = Product(name=product['name'], 
                expiry_date=product['expiry_date'], 
                volume=['volume'], 
                weight=product['weight'])
        DB.session.add(new_product)
        DB.session.commit()
        return {'status': 200}

@app.route('/product/edit/<int:id>', methods=['POST', 'DELETE'])
def product(id):
    # edit
    if request == 'POST':
        product = request.get_json()
        edit = DB.session.query(Product).filter_by(id=id).first()
        edit.name=product['name']
        edit.expiry_date=product['expiry_date'] 
        edit.volume=['volume']
        edit.weight=product['weight']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request == 'DELETE':
        edit = DB.session.query(Product).filter_by(id=id).first()
        DB.session.delete(edit)
        DB.session.commit()
        return {'status': 200}

# ######## SALESPOINTS ########### #
@app.route('/salespoints', methods=['GET', 'POST'])
def sales_points():
    # get all
    if request == 'GET':
        points = DB.session.query(SalesPoint).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'name': point.name,
                'coordinates': points.coordinates,
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request == 'POST':
        point = request.get_json()
        new_point = SalesPoint(name=point['name'], 
                coordinates=point['coordinates'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}
    
@app.route('/salespoint/edit/<int:id>', methods=['POST', 'DELETE'])
def product(id):
    # edit
    if request == 'POST':
        data = request.get_json()
        edit = DB.session.query(SalesPoint).filter_by(id=id).first()
        edit.name=data['name']
        edit.coordinates=data['coordinates'] 
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request == 'DELETE':
        data = DB.session.query(SalesPoint).filter_by(id=id).first()
        DB.session.delete(edit)
        DB.session.commit()
        return {'status': 200}

# ######## DELIVERYROUTES ########### #
@app.route('/deliveryroutes', methods=['GET', 'POST'])
def sales_points():
    # get all
    if request == 'GET':
        points = DB.session.query(DeliveryRoute).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'origin_id': point.origin_id,
                'destination_id': points.destination_id,
                'estimated_time': points.estimated_time,
                'distance': points.distance,
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request == 'POST':
        point = request.get_json()
        new_point = DeliveryRoute(origin_id=point['origin_id'], 
                destination_id=point['destination_id'],
                estimated_time=point['estimated_time'],
                distance=point['distance'],

                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}
    
@app.route('/deliveryroute/edit/<int:id>', methods=['POST', 'DELETE'])
def product(id):
    # edit
    if request == 'POST':
        data = request.get_json()
        edit = DB.session.query(DeliveryRoute).filter_by(id=id).first()
        edit.origin_id=data['origin_id']
        edit.destination_id=data['destination_id']
        edit.estimated_time=data['estimated_time']
        edit.coordinates=data['coordinates']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request == 'DELETE':
        data = DB.session.query(DeliveryRoute).filter_by(id=id).first()
        DB.session.delete(edit)
        DB.session.commit()
        return {'status': 200}


if __name__ == "__main__":
    app.run(debug=True)