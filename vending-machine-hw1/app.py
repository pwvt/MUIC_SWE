from flask import Flask, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from init_schema import *
# from sqlalchemy.sql.expression import func, desc
import yaml

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

# SQLAlchemy logging
app.config['SQLALCHEMY_ECHO'] = True

@app.route('/machines/', methods=['GET'])
def all_machines():
    machines_info = Machine.query.all()
    return ...
    # return jsonify(machines_info)
    # need to figure out how to turn sqlalchemy into json properly

@app.route('/machines/add', methods=['POST'])
def add_machine():
    mach_building = request.form['building']
    mach_loc_detail = request.form['location detail']
    
    if mach_building == "" or mach_loc_detail == "":
        return "Information not filled", 400
    new_machine = Machine(building=mach_building, location_detail=mach_loc_detail)
    db.session.add(new_machine)
    db.session.commit
    return redirect(url_for('machine', machine_id=new_machine.machine_id))


@app.route('/machines/delete', methods=['GET', 'POST'])
def delete_machine(machine_id):
    # assume there's a button on the all machines page that can delete specific machine
    machine = Machine.query.filter_by(machine_id=machine_id).first()
    if machine is None:
        return "The vending machine doesn't exist.", 400
    
    # can delete if implement cascade in database schema
    stocks = Stock.query.filter_by(machine_id=machine_id)
    stocks.delete()

    machine.delete()
    session.commit()
    return redirect(url_for('machines'))

@app.route('/machines/<int:machine_id>', methods=['GET'])
def machine(machine_id):
    machine = Machine.query.filter_by(machine_id=machine_id).first()
    return ...
    #jsonify(machine)

@app.route('/machines/<int:machine_id>/add_product', methods=['POST'])
def add_product(machine_id):
    product_name = request.form['product']
    amount = request.form['amount']

    if product_name == "" or amount == "":
        return "Information not filled.", 400

    product = Product.query.filter_by(product_name=product_name).first()

    if product is None:
        return "Product is not in database", 400
    
    new_stock = Stock(machine_id=machine_id, product_id=product.product_id, amount=amount)
    db.session.add(new_stock)
    db.session.commit
    return redirect(url_for('machine', machine_id=machine_id))

@app.route('/machines/<int:machine_id>/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(machine_id, product_id):
    # assume there's a button on the machine page that can delete specific products
    product = Product.query.filter_by(product_id=product_id).first()

    if product is None:
        return "Invalid product. The product is not in database", 400
    stock = Stock.query.filter_by(machine_id=machine_id, product_id=product_id).first()
    if stock is None:
        return "This machine doesn't have the product.", 400

    stock.delete()
    session.commit()
    return redirect(url_for('machine', machine_id=machine_id))

if __name__ == '__main__':
    app.run(debug=True)