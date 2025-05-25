from flask import Blueprint
from flask_restx import Api

from .products import products_ns
from .cart import cart_ns
from .order import order_ns

swagger_products_bp = Blueprint('swagger', __name__, url_prefix='/swagger')
api = Api(swagger_products_bp, doc='/doc', title='Documented API', description='Auto-generated Swagger Docs with Flask-RESTPlus')

api.add_namespace(products_ns, path='/api')
api.add_namespace(cart_ns, path='/api')
api.add_namespace(order_ns, path='/api')