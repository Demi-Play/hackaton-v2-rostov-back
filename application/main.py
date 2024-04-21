from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from db import Product, SalesPoint, DeliveryRoute, DeliverySchedule, Inventory, Sale, SalesForecast, SalesHistory, SeasonalFactors, MarketTrends
from flasgger import Swagger
from flask_sqlalchemy  import SQLAlchemy
from flask_cors import CORS
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soliuz.db'
CORS(app)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return response
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
        data = DB.session.query(Product).filter_by(id=id).first()
        DB.session.delete(data)
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
                'coordinates': point.coordinates,
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
        DB.session.delete(data)
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
                'destination_id': point.destination_id,
                'estimated_time': point.estimated_time,
                'distance': point.distance,
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
        DB.session.delete(data)
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
                'delivery_datetime': point.delivery_datetime,
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
        DB.session.delete(data)
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
                'quantity': point.quantity,
                'expiry_date': point.expiry_date,
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
        DB.session.delete(data)
        DB.session.commit()
        return {'status': 200}

# ######## SALE ########### #
@app.route('/sales', methods=['GET', 'POST'])
def sales():
    # get all
    if request.method == 'GET':
        points = DB.session.query(Sale).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'product_id': point.product_id,
                'sales_point_id': point.sales_point_id,
                'sale_date': point.sale_date,
                'quantity_sold': point.quantity_sold
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request.method == 'POST':
        point = request.get_json()
        new_point = Sale(product_id=point['product_id'], 
                sales_point_id=point['sales_point_id'],
                sale_date=point['sale_date'],
                quantity_sold=point['quantity_sold'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}

@app.route('/sale/edit/<int:id>', methods=['POST', 'DELETE'])
def sale(id):
    # edit
    if request.method == 'POST':
        data = request.get_json()
        edit = DB.session.query(Sale).filter_by(id=id).first()
        edit.product_id=data['product_id']
        edit.sales_point_id=data['sales_point_id']
        edit.sale_date=data['sale_date']
        edit.quantity_sold=data['quantity_sold']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request.method == 'DELETE':
        data = DB.session.query(Sale).filter_by(id=id).first()
        DB.session.delete(data)
        DB.session.commit()
        return {'status': 200}

# ######## SALESFORECAST ########### #
@app.route('/salesforecasts', methods=['GET', 'POST'])
def salesforecasts():
    # get all
    if request.method == 'GET':
        points = DB.session.query(SalesForecast).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'product_id': point.product_id,
                'sales_point_id': point.sales_point_id,
                'forecasted_demand': point.forecasted_demand,
                'avg_order_period': point.avg_order_period
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request.method == 'POST':
        point = request.get_json()
        new_point = SalesForecast(product_id=point['product_id'], 
                sales_point_id=point['sales_point_id'],
                forecasted_demand=point['forecasted_demand'],
                avg_order_period=point['avg_order_period'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}

@app.route('/salesforecast/edit/<int:id>', methods=['POST', 'DELETE'])
def salesforecast(id):
    # edit
    if request.method == 'POST':
        data = request.get_json()
        edit = DB.session.query(SalesForecast).filter_by(id=id).first()
        edit.product_id=data['product_id']
        edit.sales_point_id=data['sales_point_id']
        edit.forecasted_demand=data['forecasted_demand']
        edit.avg_order_period=data['avg_order_period']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request.method == 'DELETE':
        data = DB.session.query(SalesForecast).filter_by(id=id).first()
        DB.session.delete(data)
        DB.session.commit()
        return {'status': 200}

# ######## SALESHISTORY ########### #
@app.route('/saleshistories', methods=['GET', 'POST'])
def saleshistories():
    # get all
    if request.method == 'GET':
        points = DB.session.query(SalesHistory).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'product_id': point.product_id,
                'sale_date': point.sale_date,
                'quantity_sold': point.quantity_sold,
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request.method == 'POST':
        point = request.get_json()
        new_point = SalesHistory(product_id=point['product_id'], 
                sale_date=point['sale_date'],
                quantity_sold=point['quantity_sold'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}

@app.route('/saleshistory/edit/<int:id>', methods=['POST', 'DELETE'])
def saleshistory(id):
    # edit
    if request.method == 'POST':
        data = request.get_json()
        edit = DB.session.query(SalesHistory).filter_by(id=id).first()
        edit.product_id=data['product_id']
        edit.sale_date=data['sale_date']
        edit.quantity_sold=data['quantity_sold']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request.method == 'DELETE':
        data = DB.session.query(SalesHistory).filter_by(id=id).first()
        DB.session.delete(data)
        DB.session.commit()
        return {'status': 200}

# ######## seasonalfactors ########### #
@app.route('/seasonalfactors', methods=['GET', 'POST'])
def seasonalfactors():
    # get all
    if request.method == 'GET':
        points = DB.session.query(SeasonalFactors).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'month': point.month,
                'seasonality_coefficient': point.seasonality_coefficient,
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request.method == 'POST':
        point = request.get_json()
        new_point = SeasonalFactors(month=point['month'], 
                seasonality_coefficient=point['seasonality_coefficient'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}

@app.route('/seasonalfactor/edit/<int:id>', methods=['POST', 'DELETE'])
def seasonalfactor(id):
    # edit
    if request.method == 'POST':
        data = request.get_json()
        edit = DB.session.query(SeasonalFactors).filter_by(id=id).first()
        edit.month=data['month']
        edit.seasonality_coefficient=data['seasonality_coefficient']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request.method == 'DELETE':
        data = DB.session.query(SeasonalFactors).filter_by(id=id).first()
        DB.session.delete(data)
        DB.session.commit()
        return {'status': 200}

# ######## markettrends ########### #
@app.route('/markettrends', methods=['GET', 'POST'])
def markettrends():
    # get all
    if request.method == 'GET':
        points = DB.session.query(MarketTrends).all()
        point_list = []
        for point in points:
            point_dict = {
                'id': point.id,
                'start_date': point.start_date,
                'end_date': point.end_date,
                'trend_coefficient': point.trend_coefficient,
            }
            point_list.append(point_dict)
        return jsonify(point_list)
    # create
    if request.method == 'POST':
        point = request.get_json()
        new_point = MarketTrends(start_date=point['start_date'], 
                end_date=point['end_date'],
                trend_coefficient=point['trend_coefficient'],
                )
        DB.session.add(new_point)
        DB.session.commit()
        return {'status': 200}

@app.route('/markettrend/edit/<int:id>', methods=['POST', 'DELETE'])
def markettrend(id):
    # edit
    if request.method == 'POST':
        data = request.get_json()
        edit = DB.session.query(MarketTrends).filter_by(id=id).first()
        edit.start_date=data['start_date']
        edit.end_date=data['end_date']
        edit.trend_coefficient=data['trend_coefficient']
        DB.session.add(edit)
        DB.session.commit()
        return {'status': 200}
    # delete
    elif request.method == 'DELETE':
        data = DB.session.query(MarketTrends).filter_by(id=id).first()
        DB.session.delete(data)
        DB.session.commit()
        return {'status': 200}


if __name__ == "__main__":
    app.run(debug=True)