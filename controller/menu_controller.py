import os
import time
from flask import request, redirect, url_for, current_app, render_template
from model.menu_model import MenuModel
import logging


# Cấu hình cơ bản cho logging
logging.basicConfig(
    level=logging.DEBUG,  # Đặt mức log là DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Định dạng log
    handlers=[
        logging.StreamHandler(),  # Ghi log ra console
        logging.FileHandler("app.log")  # Ghi log vào file
    ]
)


class MenuController:
    def __init__(self):
        self.model = MenuModel()

    def request_menu(self):
        menu_items = self.model.get_menu()
        return render_template("menu.html", items=menu_items)
    
    def create_menu(self):
        return render_template("menu_form.html")
    
    def handle_upload_image(self, image_file):
        logging.debug(f"handle_upload_image image_file: {image_file}")
        logging.debug(f"handle_upload_image filename: {image_file.filename}")
        if image_file and image_file.filename != "":
            allowed_extensions = {"jpg", "jpeg", "png", "gif"}
            ext = image_file.filename.rsplit(".", 1)[-1].lower()
            
            if ext in allowed_extensions:
                # Generate a unique filename using timestamp
                image_filename = f"{int(time.time())}_{image_file.filename}"
                upload_path = os.path.join(
                    current_app.root_path, "static", "uploads", image_filename
                )

                try:
                    image_file.save(upload_path)
                    logging.debug(f"handle_upload_image image_filename: {image_filename}")
                    return image_filename
                except Exception as e:
                    logging.error(f"handle_upload_image: {e}")
                    return None
            else:
                logging.error("handle_upload_image Unsupported file extension.")
                return None
        return None

    def store_menu(self):
        # Retrieve form data
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")

        # Convert price to float
        if price:
            price = float(price)

        # Handle file upload
        image_file = request.files.get("image")
        image_filename = self.handle_upload_image(image_file)

        # Call model to store in DB
        self.model.store_menu(name, price, description, image_filename)

        # Redirect to the menu page
        return redirect(url_for("show_menu_list"))

    def list_menu(self):
        menu = self.model.get_menu()
        return render_template("list_menu.html", items=menu)

    def edit_menu(self, item_id):
        menu_item = self.model.get_menu_by_id(item_id)
        if not menu_item:
            return "Menu item not found", 404
        return render_template("edit_menu.html", item=menu_item)
    
    
    def update_menu(self, item_id):
    # Lấy dữ liệu từ form
       name = request.form.get("name")
       price = request.form.get("price")
       description = request.form.get("description")

    # Chuyển đổi giá thành float
       if price:
        price = float(price)

    # Xử lý file upload
       image_file = request.files.get("image")
       image_filename = self.handle_upload_image(image_file)

    # Cập nhật dữ liệu trong database
       self.model.update_menu(item_id, name, price, description, image_filename)
 
    # Chuyển hướng về danh sách menu
       return redirect(url_for("show_menu_list"))



    def delete_menu(self, item_id):
        self.model.delete_menu(item_id)
        return redirect(url_for("show_menu_list"))

    def view_menu(self, item_id):
        menu_item = self.model.get_menu_by_id(item_id)
        if not menu_item:
            return "Menu item not found", 404
        return render_template("view_menu.html", item=menu_item)

    def search_menu(self, query):
        menu_items = self.model.search_menu(query)
        return render_template("list_menu.html", items=menu_items)
    