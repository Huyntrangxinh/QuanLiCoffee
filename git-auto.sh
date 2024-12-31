#!/bin/bash

# Kiểm tra nếu có thay đổi trong thư mục
if [[ -n $(git status --porcelain) ]]; then
    echo "========================================="
    echo "Tự động commit và đẩy mã nguồn lên GitHub"
    echo "========================================="
    
    # Hiển thị trạng thái hiện tại
    git status
    
    # Thêm tất cả thay đổi
    echo "Thêm tất cả các file thay đổi..."
    git add .
    
    # Lấy thông điệp commit từ tham số truyền vào
    commit_message="$*"

    # Nếu không có thông điệp, gán giá trị mặc định
    if [[ -z "$commit_message" ]]; then
        commit_message="Update code automatically"
    fi
    
    # Commit thay đổi
    echo "Commit với thông điệp: $commit_message"
    git commit -m "$commit_message"
    
    # Đẩy mã nguồn lên remote repository
    echo "Đang đẩy mã nguồn lên GitHub..."
    git push
    
    echo "========================================="
    echo "Hoàn thành!"
else
    echo "========================================="
    echo "Không có thay đổi nào để commit."
    echo "========================================="
fi
