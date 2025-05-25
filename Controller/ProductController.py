from flask import Blueprint, request, jsonify
from ..Models import db
from ..Models.ProductsModel import Product

product_api = Blueprint('products', __name__)


@product_api.route("/products", methods=['GET']) # requested by Product List with or without search params (query)
@product_api.route("/product/<id>", methods=['GET']) # requested by product detail page (id)
def get_products(id=None):
    args = request.args.to_dict()
    query = args.get("query")

    if(args.get("pageSize") and args.get("currentPage")):
        page_size = int(args.get("pageSize"))
        current_page = int(args.get("currentPage"))
    else:
        page_size = 10
        current_page = 1

    if(query is None and id is not None): # return product base on id, 
        
        product = Product.query.filter(Product.id==id).first()
        return jsonify(product.serialized) if product else jsonify({'error': 'Produto não encontrado'}), 404

    elif(query is None and id is None): # return all products
        
        all_products = Product.query

    elif(query is not None and id is None): # return products base on search params
        
        all_products = Product.query.filter(
            Product.title.ilike(f'%{query}%'))
    
    pagination = all_products.paginate(page=current_page, per_page=page_size, error_out=False)

    return jsonify({
        'query': query, 
        'pageSize': page_size, 
        'currentPage': current_page, 
        'totalItems': pagination.total, 
        'totalPages': pagination.pages, 
        'results': [p.serialized for p in pagination.items]
        })
    

def run_products(app):

    with app.app_context():
      
        if Product.query.count() == 0:
            product1 = Product(
                title="Caneca Azul", 
                amount=123.45, 
                installments=3, 
                installments_fee=False)
            product2 = Product(
                title="Caneca Vermelha", 
                amount=100.23, 
                installments=4, 
                installments_fee=True)
            product3 = Product(
                title="Caneca Amarela", 
                amount=145.20, 
                installments=6, 
                installments_fee=True,)
            product4 = Product(
                title="Caneca Arco-Íris", 
                amount=80.34, 
                installments=3, 
                installments_fee=False)
            product5 = Product(
                title="Caneca Roxa", 
                amount=90.12, 
                installments=4, 
                installments_fee=True)
            product6 = Product(
                title="Caneca Preta", 
                amount=74.78, 
                installments=6, 
                installments_fee=True)

            db.session.add_all([product1, product2, product3, product4, product5, product6])
            db.session.commit()
