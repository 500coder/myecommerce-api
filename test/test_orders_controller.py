from ..Controller.OrdersController import sum_total
from flask import json

def test_sum_total():
    
    # given
    cart_string = """
        {
            "code": "fixed-cart-code",
            "created_at": "2025-05-23T01:52:41.704603",
            "id": 1,
            "products": [
                {
                    "id": "1",
                    "quantity": 2,
                    "thumbnailUrl": "https://placehold.co/100",
                    "title": "Caneca Azul",
                    "unitPrice": "123.45"
                },
                {
                    "id": "3",
                    "quantity": 1,
                    "thumbnailUrl": "https://placehold.co/100",
                    "title": "Caneca Amarela",
                    "unitPrice": "145.20"
                },
                {
                    "id": "4",
                    "quantity": 1,
                    "thumbnailUrl": "https://placehold.co/100",
                    "title": "Caneca Arco-\u00cdris",
                    "unitPrice": "80.34"
                }
            ],
            "updated_at": "2025-05-23T01:53:29.686798"
        }
        """
    cart_json = json.loads(cart_string)

    expected = 472.44

    actual = sum_total(cart_json['products'])

    assert expected == actual