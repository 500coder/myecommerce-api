from flask_restx import Namespace, Resource, fields
from ..Models.ProductsModel import Product as ProductModel
from flask import jsonify, request

products_ns = Namespace('Products', description='Products operations')

# Response models
installment_model = products_ns.model('Installments', {
        "fee": fields.Boolean(description='Has fee'),
        "number": fields.Integer(description='Quantity of installment'),
        "total": fields.Float(description='Price of each installment'),
      })

product_model = products_ns.model('Product', {
      "amount": fields.Float(description='Price of product'),
      "id": fields.Integer(description='Product id'),
      "installments": fields.Nested(installment_model, description='Intallments details'),
      "title": fields.String(description='Product title (or names)')
    })

products_model = products_ns.model('Products', {
    'query': fields.String(description='Product search query'),
    'pageSize': fields.Integer(description='Items per page'),
    'currentPage': fields.Integer(description='Current page number'),
    'totalItems': fields.Integer(description='Total number of items'),
    'totalPages': fields.Integer(description='Total number of pages'),
    'results': fields.List(fields.Nested(product_model), description='List of products'),
})

@products_ns.route('/product')
class Products(Resource):
    @products_ns.response(200, 'Success', products_model)
    @products_ns.response(500, 'Internal Server Error')
    @products_ns.doc(params={'query': 'Product title to search'})
    def get(self):
        '''Returns a list of products'''

        # Get query params
        query = request.args.get('query', '', type=str)
        current_page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)

        # Database query with filter
        all_products = ProductModel.query.filter(ProductModel.title.ilike(f'%{query}%'))
        pagination = all_products.paginate(page=current_page, per_page=page_size, error_out=False)

        return jsonify({
            'query': query,
            'pageSize': page_size,
            'currentPage': current_page,
            'totalItems': pagination.total,
            'totalPages': pagination.pages,
            'results': [p.serialized for p in pagination.items]
        })


@products_ns.route('/product/<id>')
class Product(Resource):
    @products_ns.response(200, 'Success', product_model)
    @products_ns.response(404, 'Product not found')
    
    def get(self, id):
        '''Returns destails of a product'''
        product = ProductModel.query.filter(ProductModel.id==id).first()
        return jsonify(product.serialized) 
