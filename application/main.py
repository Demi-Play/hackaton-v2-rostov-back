from flask import Flask, jsonify
from flask_restful import Api, Resource
from db import Product
from flasgger import Swagger
from flask_sqlalchemy  import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soliuz.db'

DB = SQLAlchemy(app)


swagger = Swagger(app)

class HelloWorld(Resource):
    """
    This is the description for HelloWorld resource
    """

    def get(self):
        """
        This is the description for GET method
        It returns a simple Hello World message
        ---
        responses:
          200:
            description: A simple hello world message
        """
        products = DB.session.query(Product).all()
        product_list = []
        for product in products:
            user_dict = {
                'id': product.id,
                'name': product.name,
                'expiry_date': product.expiry_date,
                'volume': product.volume,
                'weight': product.weight
            }
            product_list.append(user_dict)
        return jsonify(product_list)


class Add(Resource):
    """
    This is the description for Add resource
    """

    def post(self, num1, num2):
        """
        This is the description for POST method
        It adds two numbers and returns the result
        ---
        parameters:
          - name: num1
            in: path
            type: int
            required: true
            description: The first number
          - name: num2
            in: path
            type: int
            required: true
            description: The second number
        responses:
          200:
            description: The sum of two numbers
        """
        return {"result": num1 + num2}


api.add_resource(HelloWorld, "/")
api.add_resource(Add, "/add/<int:num1>/<int:num2>")

if __name__ == "__main__":
    app.run(debug=True)