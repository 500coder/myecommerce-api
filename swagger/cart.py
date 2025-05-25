from flask_restx import Namespace, Resource, fields
from ..Models.CartModel import Cart as CartModel
from flask import jsonify, request
from .products import product_model
from ..Controller.CartController import update_cart

cart_ns = Namespace('Cart', description='Cart operations')
cart_model = cart_ns.model('cart',  {
    "code": fields.String(description='cart unique code - acts as a identifier'),
    "created_at": fields.DateTime(description='Cart creation timestamp'),
    "id": fields.String(description='cart internal id'),
    "products": fields.List(fields.Nested(product_model), description='List of products'),
    "updated_at": fields.DateTime(description='Cart update timestamp')
})

carts_model = cart_ns.model('carts',  {
  "carts": fields.Nested(cart_model, description='Carts')
})

# cart_update_model = {

# }


@cart_ns.route('/cart')
class Carts(Resource):
    '''Returns a list of carts'''
    @cart_ns.response(200, 'Success', carts_model)
    @cart_ns.response(500, 'Internal Server Error')
    def get(self):
        carts = CartModel.query.all()
        return jsonify({'carts': c.serialized for c in carts})
    

@cart_ns.route('/cart/<cart_code>')
@cart_ns.param('cart_code', 'The cart unique code')
class Cart(Resource):
    @cart_ns.response(200, 'Success', cart_model)
    @cart_ns.response(500, 'Internal Server Error')

    def get(self, cart_code):
        '''Returns details of a cart'''
        cart = CartModel.query.filter(CartModel.code == cart_code).one()
        return jsonify(cart.serialized)
    
    # @cart_ns.expect(cart_update_model)
    def put(self, cart_code):
        '''Updates a cart'''
        try:
            payload = request.get_json()
            if not payload:
                return {'message': 'No input data provided'}, 400
            result = update_cart(payload, cart_code)
            return result, 200
        except Exception as e:
            return {'message': str(e)}, 500