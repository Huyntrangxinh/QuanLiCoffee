# model/order_model.py
import sqlite3
import logging
from datetime import datetime

class OrderModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def create_order(self, order_code, items, total_price, note):
        """
        Tạo một order mới và lưu vào bảng orders
        """
        logging.debug(f"create_order: {order_code}, total={total_price}, note={note}")
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        created_at = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO orders (order_code, items, total_price, note, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (order_code, items, total_price, note, created_at))

        connection.commit()
        connection.close()

    def get_all_orders(self):
        """
        Lấy tất cả đơn hàng trong bảng orders, trả về list dict
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, order_code, items, total_price, note, created_at
            FROM orders
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        connection.close()

        orders = []
        for row in rows:
            oid, order_code, items, total_price, note, created_at,  = row
            orders.append({
                "id": oid,
                "order_code": order_code,
                "items": items,
                "total_price": total_price,
                "note": note,
                "created_at": created_at,
            })
        return orders

    def get_order_by_id(self, order_id):
        """
        Lấy thông tin 1 order theo ID
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, order_code, items, total_price, note, created_at
            FROM orders
            WHERE id = ?
        """, (order_id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            oid, order_code, items, total_price, note, created_at = row
            return {
                "id": oid,
                "order_code": order_code,
                "items": items,
                "total_price": total_price,
                "note": note,
                "created_at": created_at,
            }
        return None

    def update_order(self, order_id, order_code, items, total_price, note ):
        """
        Cập nhật 1 order có sẵn trong bảng.
        Cho phép thay đổi order_code, items, total_price, note
        """
        logging.debug(f"update_order ID={order_id}, code={order_code}, total={total_price}")
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE orders
            SET order_code = ?,
                items = ?,
                total_price = ?,
                note = ?,
            WHERE id = ?
        """, (order_code, items, total_price, note, order_id))

        connection.commit()
        connection.close()

    def delete_order(self, order_id):
        """
        Xoá 1 order khỏi bảng orders
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        connection.commit()
        connection.close()
