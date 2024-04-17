from flask import Flask, request, render_template, session, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import *


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
migrate = Migrate(app, db)

VIDKRILO
def get_pagination_args(args):
    if 'page' not in args.keys():
        page = 1
    else:
        page = args['page']
    return page


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))
    price = db.Column(db.Float)
    img = db.Column(db.String(256))


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/cart/add/<product_id>', methods=['POST'])
def add_product_to_cart(product_id):
    product = Product.query.filter_by(id=int(product_id)).first()

    if not product:
        abort(404)

    if 'cart' not in session:
        session['cart'] = {'products': []}

    for cart_product in session['cart']['products']:
        if cart_product['id'] == product.id:
            cart_product['quantity'] += 1
            cart_product['price'] = float(cart_product['price']) + float(product.price)
            break
    else:
        session['cart']['products'].append(
            {
                'id': product.id,
                'name': product.name,
                'quantity': 1,
                'price': float(product.price),
                'img': product.img,
            }
        )
    session.modified = True

    return redirect(url_for('cart_product_all'))


@app.route('/cart/remove/<product_id>', methods=['GET', 'POST'])
def remove_product_from_cart(product_id):
    if 'cart' in session and 'products' in session['cart']:
        for index, cart_product in enumerate(session['cart']['products']):
            if cart_product['id'] == int(product_id):
                del session['cart']['products'][index]
                break
    session.modified = True
    return redirect(url_for('cart_product_all'))


@app.route('/cart/decrease/<product_id>', methods=['POST'])
def remove_one_product_from_cart(product_id):
    product = Product.query.filter_by(id=int(product_id)).first()

    if not product:
        abort(404)

    if 'cart' not in session:
        return redirect('/')

    for cart_product in session['cart']['products']:
        if cart_product['id'] == product.id:
            if cart_product['quantity'] == 1:
                remove_product_from_cart(product.id)
            else:
                cart_product['quantity'] -= 1
                cart_product['price'] = float(cart_product['price']) - float(product.price)
            break

    session.modified = True

    return redirect(url_for('cart_product_all'))


@app.route('/cart/all')
def cart_product_all():
        cart = []
        quantity = 1

        if 'cart' in session and 'products' in session['cart']:
            cart = session['cart']['products']
        else:
            cart = []

        cart = session.get('cart', {}).get('products', [])

        total_price = 0

        for product in cart:
            try:
                price_str = str(product.get('price', '0'))
                price_str = price_str.replace('$', '')
                price = float(price_str)
                quantity = int(product.get('quantity', 0))
                product_total_price = price
                total_price += product_total_price
                product['total_price'] = product_total_price

            except ValueError:
                print(f"Invalid price or quantity for product: {product}")

        total_products_price = float(sum(product.get('total_price', 0)for product in cart))

        return render_template('cart.html', cart=cart, total_price=total_price,
                               quantity=quantity, total_products_price=total_products_price)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/menu', methods=['GET'])
def menu():
    page = get_pagination_args(request.args)
    if int(page) == 0:
        page = 1
    products = Product.query.paginate(page=int(page), per_page=5)
    return render_template('menu.html', products=products, page=int(page))


@app.route('/about-us')
def about_us():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)