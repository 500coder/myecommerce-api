from flask_restx import Namespace, Resource, fields

order_ns = Namespace('Order', description='Order operations')
# order_model = order_ns.model()