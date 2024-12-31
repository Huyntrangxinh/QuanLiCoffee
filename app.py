from flask import Flask, render_template, request, redirect, url_for, session
from controller.menu_controller import MenuController
from controller.order_controller import OrderController

app = Flask(__name__)
app.secret_key = "some-secret-key"  # Thay bằng chuỗi bí mật bất kỳ

# --------------------------------------------------------------
# BỘ EMAIL / PASSWORD ADMIN GIẢ LẬP
# --------------------------------------------------------------
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

# --------------------------------------------------------------
# ROUTE LOGIN/LOGOUT (GIẢ LẬP)
# --------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    GET: Hiển thị form đăng nhập
    POST: Xử lý form đăng nhập
    """
    if request.method == "GET":
        return render_template("login.html")  # Form login (sẽ tạo ở templates/login.html)
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        # Kiểm tra cứng xem có trùng ADMIN_EMAIL và ADMIN_PASSWORD không
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session["user_role"] = "admin"
            return redirect(url_for("show_menu_list"))  # Về trang admin menu
        else:
            return "Sai email hoặc password!", 401

@app.route("/logout")
def logout():
    """
    Logout: xóa session để mất quyền admin
    """
    session.pop("user_role", None)
    return "Bạn vừa đăng xuất! <a href='/'>Về trang chủ</a>"

# --------------------------------------------------------------
# ROUTES CHO MENU
# --------------------------------------------------------------
@app.route("/")
def show_menu():
    controller = MenuController()
    return controller.request_menu()

@app.route("/menu/edit/<int:item_id>", methods=["GET"])
def edit_menu(item_id):
    controller = MenuController()
    return controller.edit_menu(item_id)

@app.route("/menu/update/<int:item_id>", methods=["POST"])
def update_menu(item_id):
    controller = MenuController()
    return controller.update_menu(item_id)

@app.route("/admin/")
@app.route("/admin/menu/manager")
def show_menu_list():
    # Kiểm tra nếu không phải admin -> chặn
    if session.get("user_role") != "admin":
        return "Access denied", 403

    controller = MenuController()
    return controller.list_menu()

@app.route("/admin/menu/create")
def create_menu():
    if session.get("user_role") != "admin":
        return "Access denied", 403

    controller = MenuController()
    return controller.create_menu()

@app.route("/admin/menu/store", methods=["POST"])
def store_menu():
    if session.get("user_role") != "admin":
        return "Access denied", 403

    controller = MenuController()
    return controller.store_menu()

@app.route("/menu/remove/<int:item_id>", methods=["GET"])
def remove_menu(item_id):
    if session.get("user_role") != "admin":
        return "Access denied", 403

    controller = MenuController()
    return controller.delete_menu(item_id)

# --------------------------------------------------------------
# ROUTES CHO GIỎ HÀNG (CART)
# --------------------------------------------------------------
@app.route("/cart/add/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    """Thêm món vào session cart."""
    quantity = request.form.get("quantity", 1, type=int)

    # Lấy giỏ từ session (nếu chưa có thì tạo rỗng)
    cart = session.get("cart", {})
    
    # Nếu có rồi thì tăng số lượng, chưa có thì thêm mới
    if str(item_id) in cart:
        cart[str(item_id)]["quantity"] += quantity
    else:
        # Lấy thông tin món từ MenuModel
        menu_controller = MenuController()
        menu_item = menu_controller.model.get_menu_by_id(item_id)
        if not menu_item:
            return "Item not found", 404
        
        cart[str(item_id)] = {
            "name": menu_item["name"],
            "price": menu_item["price"],
            "quantity": quantity
        }
    
    # Lưu lại cart vào session
    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.route("/cart")
def view_cart():
    """Xem giỏ hàng."""
    cart = session.get("cart", {})
    total_price = sum(item["price"] * item["quantity"] for item in cart.values())
    return render_template("cart.html", cart=cart, total_price=total_price)

@app.route("/cart/checkout", methods=["POST"])
def checkout():
    """Khi user nhấn Submit Order, lưu DB, xoá session giỏ."""
    from model.order_model import OrderModel  # import tạm ngay trong hàm
    import json, uuid

    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("view_cart"))

    note = request.form.get("note", "")
    total_price = sum(item["price"] * item["quantity"] for item in cart.values())

    # Tạo mã đơn (đơn giản: ORD + 8 ký tự random)
    order_code = "ORD-" + str(uuid.uuid4())[:8]

    # Convert cart thành JSON để lưu DB
    items_json = json.dumps(cart)

    # Gọi OrderModel để lưu
    order_model = OrderModel()
    order_model.create_order(order_code, items_json, total_price, note)

    # Xoá giỏ
    session["cart"] = {}

    return render_template("order_success.html", order_code=order_code)

# --------------------------------------------------------------
# ROUTES CHO ORDER (ADMIN)
# --------------------------------------------------------------
@app.route("/admin/manager/order", methods=["GET"])
def show_order_list():
    """Xem tất cả đơn hàng (ADMIN)."""
    if session.get("user_role") != "admin":
        return "Access denied", 403

    controller = OrderController()
    return controller.list_orders()

@app.route("/admin/manager/order/view/<int:order_id>", methods=["GET"])
def view_order_detail(order_id):
    """Xem chi tiết 1 đơn hàng (ADMIN)."""
    if session.get("user_role") != "admin":
        return "Access denied", 403

    controller = OrderController()
    return controller.view_order(order_id)

@app.route("/admin/manager/order/edit/<int:order_id>", methods=["GET", "POST"])
def edit_order(order_id):
    """Sửa 1 đơn hàng (ADMIN)."""
    if session.get("user_role") != "admin":
        return "Access denied", 403

    controller = OrderController()
    if request.method == "GET":
        return controller.view_order(order_id)
    else:
        return controller.update_order(order_id)

@app.route("/admin/manager/order/delete/<int:order_id>", methods=["GET"])
def remove_order(order_id):
    """Xoá 1 đơn hàng."""
    if session.get("user_role") != "admin":
        return "Access denied", 403

    controller = OrderController()
    return controller.delete_order(order_id)

# --------------------------------------------------------------
# CHẠY ỨNG DỤNG
# --------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
