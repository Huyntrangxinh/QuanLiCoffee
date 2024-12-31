import sqlite3

def add_image_column(db_path="database.db"):
    """
    Thêm cột 'image' vào bảng 'menus' (nếu bảng và cột chưa tồn tại).
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE menus ADD COLUMN image TEXT")
        connection.commit()
        print("Added 'image' column to 'menus' table.")
    except sqlite3.OperationalError as e:
        # Nếu cột đã tồn tại, SQLite sẽ báo lỗi
        if "duplicate column name" in str(e).lower():
            print("Column 'image' already exists in 'menus' table.")
        else:
            raise e
    finally:
        connection.close()

def create_orders_table(db_path="database.db"):
    """
    Tạo bảng 'orders' (nếu chưa có).
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_code TEXT NOT NULL,
                items TEXT,
                total_price REAL,
                note TEXT,
                created_at TEXT,
            );
        """)
        connection.commit()
        print("Table 'orders' has been created (if it didn't exist).")
    except Exception as e:
        print(f"Error creating 'orders' table: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    # Gọi các hàm bên trên
    add_image_column()
    create_orders_table()
