from flask import Blueprint, request, jsonify, json

from ..Models import db
from ..Models.OrdersModel import Orders
from .CartController import get_by_code
from datetime import datetime, timezone
from decimal import *

order_api = Blueprint('orders', __name__)

@order_api.route("/order/", methods=['POST'])
def order():
    payload = request.get_json()
    cart_code = payload['cart_code']
    order = create_from(cart_code)

    return jsonify(order.serialized)


def create_from(cart_code):

    with db.session.begin():
        cart = get_by_code(cart_code)
        now = datetime.now(timezone.utc)
        order = Orders(products=cart.content, amount=sum_total(cart.serialized['products']), created_at=now, updated_at=now, status='DONE')
    
        db.session.add(order)
        db.session.commit()

        return order


def sum_total(cart):
    total = 0
    for p in cart:
        total = total + (Decimal(p['unitPrice']) * int(p['quantity']))
    return float(round(total, 2))