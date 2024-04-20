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
    if request.method == 'GET':
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
    if request.method == 'POST':
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
    if request.method == 'POST':
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
    elif request.method == 'DELETE':
        edit = DB.session.query(Product).filter_by(id=id).first()
        DB.session.delete(edit)
        DB.session.commit()
        return {'status': 200}

# ######## SALESPOINTS ########### #
@app.route('/salespoints', methods=['GET', 'POST'])
def sales_points():
    # get all
    if request.method == 'GET':
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
    if request.method == 'POST':
        point = request.get_json()
        new_point = SalesPoint(name=point['name'], 
                coordinates=point['coordinates'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}
    
@app.route('/salespoint/edit/<int:id>', methods=['POST', 'DELETE'])
def sales_point(id):
    # edit
    if request.method == 'POST':
        data = request.get_json()
        edit = DB.session.query(SalesPoint).filter_by(id=id).first()
        edit.name=data['name']
        edit.coordinates=data['coordinates'] 
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request.method == 'DELETE':
        data = DB.session.query(SalesPoint).filter_by(id=id).first()
        DB.session.delete(edit)
        DB.session.commit()
        return {'status': 200}

# ######## DELIVERYROUTES ########### #
@app.route('/deliveryroutes', methods=['GET', 'POST'])
def delivery_routes():
    # get all
    if request.method == 'GET':
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
    if request.method == 'POST':
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
def delivery_route(id):
    # edit
    if request.method == 'POST':
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
    elif request.method == 'DELETE':
        data = DB.session.query(DeliveryRoute).filter_by(id=id).first()
        DB.session.delete(edit)
        DB.session.commit()
        return {'status': 200}

# ######## DELIVERYSCHEDULE ########### #
@app.route('/deliveryschedules', methods=['GET', 'POST'])
def delivery_schedules():
    # get all
    if request.method == 'GET':
        points = DB.session.query(DeliveryRoute).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'route_id': point.route_id,
                'delivery_datetime': points.delivery_datetime,
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request.method == 'POST':
        point = request.get_json()
        new_point = DeliveryRoute(route_id=point['route_id'], 
                delivery_datetime=point['delivery_datetime'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}
    
@app.route('/deliveryschedule/edit/<int:id>', methods=['POST', 'DELETE'])
def delivery_schedule(id):
    # edit
    if request.method == 'POST':
        data = request.get_json()
        edit = DB.session.query(DeliverySchedule).filter_by(id=id).first()
        edit.route_id=data['route_id']
        edit.delivery_datetime=data['delivery_datetime']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request.method == 'DELETE':
        data = DB.session.query(DeliverySchedule).filter_by(id=id).first()
        DB.session.delete(edit)
        DB.session.commit()
        return {'status': 200}

# ######## INVENTORY ########### #
@app.route('/inventories', methods=['GET', 'POST'])
def inventories():
    # get all
    if request.method == 'GET':
        points = DB.session.query(Inventory).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'product_id': point.product_id,
                'quantity': points.quantity,
                'expiry_date': points.expiry_date,
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request.method == 'POST':
        point = request.get_json()
        new_point = Inventory(product_id=point['product_id'], 
                quantity=point['quantity'],
                expiry_date=point['expiry_date'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}
    
@app.route('/inventory/edit/<int:id>', methods=['POST', 'DELETE'])
def inventory(id):
    # edit
    if request.method == 'POST':
        data = request.get_json()
        edit = DB.session.query(Inventory).filter_by(id=id).first()
        edit.product_id=data['product_id']
        edit.quantity=data['quantity']
        edit.expiry_date=data['expiry_date']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request.method == 'DELETE':
        data = DB.session.query(Inventory).filter_by(id=id).first()
        DB.session.delete(edit)
        DB.session.commit()
        return {'status': 200}



if __name__ == "__main__":
    app.run(debug=True)