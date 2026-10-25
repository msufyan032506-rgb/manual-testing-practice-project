from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = "practice-only-secret-key"

# Demo accounts only. Do not use real passwords.
USERS = {
    "tester@example.com": {"password": "Test123!", "name": "Demo Tester"}
}
PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "price": 1200, "description": "Comfortable wireless mouse."},
    {"id": 2, "name": "USB Keyboard", "price": 1800, "description": "Compact USB keyboard."},
    {"id": 3, "name": "Headphones", "price": 2500, "description": "Wired headphones for daily use."},
    {"id": 4, "name": "Laptop Stand", "price": 2200, "description": "Adjustable desk stand."},
    {"id": 5, "name": "USB-C Cable", "price": 500, "description": "One-metre charging cable."},
    {"id": 6, "name": "Notebook", "price": 250, "description": "A5 ruled notebook."},
]

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_email" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

def cart_items():
    cart = session.get("cart", {})
    items = []
    total = 0
    for product in PRODUCTS:
        qty = int(cart.get(str(product["id"]), 0))
        if qty > 0:
            subtotal = qty * product["price"]
            items.append({**product, "quantity": qty, "subtotal": subtotal})
            total += subtotal
    return items, total

@app.context_processor
def inject_globals():
    cart = session.get("cart", {})
    return {"cart_count": sum(int(q) for q in cart.values())}

@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS[:3])

@app.route("/products")
def products():
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "all")
    result = PRODUCTS
    if query:
        result = [p for p in result if query in p["name"].lower() or query in p["description"].lower()]
    if category == "budget":
        result = [p for p in result if p["price"] < 1500]
    elif category == "premium":
        result = [p for p in result if p["price"] >= 1500]
    return render_template("products.html", products=result, q=request.args.get("q", ""), category=category)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = USERS.get(email)
        if user and user["password"] == password:
            session["user_email"] = email
            flash("Welcome back, " + user["name"] + "!", "success")
            return redirect(request.args.get("next") or url_for("home"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_email", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)

@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products"))
    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        quantity = 1
    if quantity < 1 or quantity > 99:
        flash("Quantity must be between 1 and 99.", "error")
        return redirect(request.referrer or url_for("products"))
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = int(cart.get(key, 0)) + quantity
    session["cart"] = cart
    flash(f"Added {quantity} × {product['name']} to cart.", "success")
    return redirect(request.referrer or url_for("products"))

@app.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    cart = session.get("cart", {})
    key = str(product_id)
    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        quantity = 1
    if key not in cart:
        flash("That item is not in your cart.", "error")
    elif quantity <= 0:
        cart.pop(key, None)
        session["cart"] = cart
        flash("Item removed from cart.", "success")
    elif quantity > 99:
        flash("Quantity cannot exceed 99.", "error")
    else:
        cart[key] = quantity
        session["cart"] = cart
        flash("Cart updated.", "success")
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_items()
    if not items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        city = request.form.get("city", "").strip()
        address = request.form.get("address", "").strip()
        if not name or not city or not address:
            flash("Please complete all required fields.", "error")
            return render_template("checkout.html", items=items, total=total)
        # Demo only: no real payment and no order persistence.
        session["last_order"] = {"name": name, "city": city, "address": address, "total": total}
        session["cart"] = {}
        return redirect(url_for("order_confirmation"))
    return render_template("checkout.html", items=items, total=total)

@app.route("/order-confirmation")
def order_confirmation():
    order = session.get("last_order")
    if not order:
        flash("No recent demo order found.", "warning")
        return redirect(url_for("home"))
    return render_template("confirmation.html", order=order)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please fill in all fields.", "error")
        elif "@" not in email or "." not in email.split("@")[-1]:
            flash("Please enter a valid email address.", "error")
        else:
            flash("Thanks! Your demo message has been received.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "Manual Testing Practice Shop"})

if __name__ == "__main__":
    app.run(debug=True)
