from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func, select, case
# from sqlalchemy.orm import aliased

from flask import Flask
import yaml

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)

# from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + cred['mysql_user'] + ':' + cred['mysql_password'] + '@' + cred['mysql_host'] + '/' + cred['mysql_db']
app.config['SQLALCHEMY_ECHO'] = True

print(app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)

# create tables

# stocks = db.Table('stocks', 
#     db.Column(db.Integer, db.ForeignKey("machine.machine_id"), primary_key = True),
#     db.Column(db.Integer, db.ForeignKey("product.product_id"), primary_key = True),
#     db.Column(db.Integer())
# )

class Stock( db.Model ): # relationship between machine and product
    machine_id      = db.Column(db.Integer, db.ForeignKey("machine.machine_id"), primary_key = True)
    product_id      = db.Column(db.Integer, db.ForeignKey("product.product_id"), primary_key = True)
    amount          = db.Column(db.Integer())
    machine         = db.relationship("Machine", back_populates="products")
    product         = db.relationship("Product", back_populates="machines")

    def __init__(self, machine_id, product_id, amount):
        self.machine_id = machine_id
        self.product_id = product_id
        self.amount = amount

class Machine( db.Model ):
    machine_id      = db.Column(db.Integer, primary_key = True, autoincrement=True)
    building        = db.Column(db.String(50), nullable=False)
    location_detail = db.Column(db.String(150), nullable=False)
    products        = db.relationship('Stock', back_populates="machine")
    
    def __init__(self, building, location_detail):
        self.building = building
        self.location_detail = location_detail

class Product( db.Model ):
    product_id      = db.Column(db.Integer, primary_key = True, autoincrement=True)
    product_name    = db.Column(db.String(50), unique=True, nullable=False)
    product_type       = db.Column(db.String(50))
    price           = db.Column(db.Float, nullable=False)
    machines        = db.relationship("Stock", back_populates="product")

    def __init__(self, product_name, price):
        self.product_name = product_name
        self.price = price

def create():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':  
    with app.app_context():
        create()

