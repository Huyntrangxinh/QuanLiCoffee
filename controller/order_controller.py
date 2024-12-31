# order_controller.py
import logging
import json
from flask import render_template, request, redirect, url_for
from model.order_model import OrderModel

class OrderController:
    def __init__(self):
        self.model = OrderModel()

    def list_orders(self):
        """
        Lấy danh sách tất cả đơn hàng từ model và hiển thị.
        Trong cột 'items' đang lưu JSON, ta parse ra dict 
        để template có thể lặp và hiển thị món trong đơn.
        """
        orders = self.model.get_all_orders()
        for o in orders:
            # o["items"] là chuỗi JSON => parse sang dict
            if o["items"]:
                o["items"] = json.loads(o["items"])
            else:
                o["items"] = {}
        return render_template("list_order.html", orders=orders)

    def view_order(self, order_id):
        """
        Hiển thị chi tiết 1 đơn hàng (theo ID).
        """
        order = self.model.get_order_by_id(order_id)
        if not order:
            return "Order not found", 404

        # Parse JSON 'items' thành dict
        if order["items"]:
            order["items"] = json.loads(order["items"])
        else:
            order["items"] = {}

        return render_template("view_order.html", order=order)

    def new_order(self):
        """
        Render form tạo đơn hàng (nếu cần tạo thủ công).
        """
        return render_template("order_form.html")

    def store_order(self):
        """
        Xử lý khi submit form tạo đơn hàng (nếu tạo thủ công).
        """
        order_code = request.form.get("order_code")
        items = request.form.get("items")  # Chuỗi JSON hoặc text
        total_price = request.form.get("total_price")
        note = request.form.get("note")

        # Convert total_price sang float
        if total_price:
            total_price = float(total_price)

        # Gọi model để lưu DB
        # Ở model, create_order(...) nên có tham số status
        self.model.create_order(order_code, items, total_price, note)
        return redirect(url_for("show_order_list"))

    def update_order(self, order_id):
        """
        Cập nhật nội dung 1 đơn hàng.
        (Ví dụ: thay đổi items, total_price, note, status)
        """
        order_code = request.form.get("order_code")
        items = request.form.get("items")
        total_price = request.form.get("total_price")
        note = request.form.get("note")

        # Convert total_price sang float
        if total_price:
            total_price = float(total_price)

        # Gọi model.update_order(...) truyền cả status
        self.model.update_order(order_id, order_code, items, total_price, note)
        return redirect(url_for("show_order_list"))

    def delete_order(self, order_id):
        """
        Xoá đơn hàng.
        """
        self.model.delete_order(order_id)
        return redirect(url_for("show_order_list"))
