"""
Flask routes for GLH platform.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app import db, bcrypt
from app.models import User, Product, Producer, Order, Loyalty
from flask_login import login_user, logout_user, login_required, current_user
import pandas as pd

main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/")
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)


@main_routes.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_producer:
        return "Access denied - producers only."

    products = Product.query.filter_by(producer_id=current_user.id).all()
    return render_template("dashboard.html", products=products)


@main_routes.route("/order/<int:product_id>", methods=["POST"])
@login_required
def order_product(product_id):
    quantity = int(request.form["quantity"])
    product = Product.query.get_or_404(product_id)

    if quantity > product.stock:
        return "Not enough stock."

    product.stock -= quantity

    new_order = Order(
        user_id=current_user.id,
        product_id=product_id,
        quantity=quantity
    )

    # Loyalty points: 1 point per £10 spent
    points = int(product.price * quantity // 10)

    loyalty = Loyalty.query.filter_by(user_id=current_user.id).first()

    if loyalty:
        loyalty.points += points
    else:
        loyalty = Loyalty(user_id=current_user.id, points=points)
        db.session.add(loyalty)

    db.session.add(new_order)
    db.session.commit()

    return redirect(url_for("main_routes.home"))


@main_routes.route("/import_csv")
def import_csv():
    """Import sample product data using Pandas."""
    try:
        df = pd.read_csv("csv/sample_products.csv")
    except FileNotFoundError:
        return "CSV file not found."

    for _, row in df.iterrows():
        product = Product(
            name=row["name"],
            price=row["price"],
            stock=row["stock"],
            description=row["description"],
            producer_id=1  # Example producer
        )
        db.session.add(product)

    db.session.commit()
    return "CSV Imported Successfully!"


@main_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        # Check for existing user
        if User.query.filter_by(username=username).first():
            return "Username already exists"

        password = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main_routes.home"))

    return render_template("register.html")


@main_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("main_routes.home"))
        else:
            return "Invalid login"

    return render_template("login.html")


@main_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_routes.home"))


@main_routes.route("/update_stock/<int:product_id>", methods=["POST"])
@login_required
def update_stock(product_id):
    product = Product.query.get_or_404(product_id)

    if product.producer_id != current_user.id:
        return "Permission denied."

    new_stock = int(request.form["stock"])
    product.stock = new_stock

    db.session.commit()
    return redirect(url_for("main_routes.dashboard"))