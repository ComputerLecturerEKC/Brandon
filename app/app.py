import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import csv

path = os.getcwd()

app = Flask(__name__)

# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Product details
class LocalCompanyData(db.Model):
    productId = db.Column(db.Integer, primary_key=True)
    productType = db.Column(db.String(50))
    productFamily = db.Column(db.String(50))
    productSource = db.Column(db.String(50))
    productWholesalePrice = db.Column(db.Float)
    productRRPprice = db.Column(db.Float)
    profitability = db.Column(db.Float)

# Create tables (run once)
with app.app_context():
    db.create_all()

# display a main form using routing
@app.route('/add', methods=['GET'])
def add_form():
    return render_template("add.html")

# run app
if __name__ == "__main__":
    app.run(debug=True)


