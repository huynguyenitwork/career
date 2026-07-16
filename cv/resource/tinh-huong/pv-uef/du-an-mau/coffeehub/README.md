# =============================================
# 📁 Cấu trúc thư mục
# =============================================
# CoffeeHub/
# ├── services/
# │ ├── user-service/
# │ │ ├── Dockerfile
# │ │ └── Program.cs
# │ ├── order-service/
# │ │ ├── Dockerfile
# │ │ └── Program.cs
# │ ├── product-service/
# │ │ ├── Dockerfile
# │ │ └── Program.cs
# ├── ai-service/
# │ ├── Dockerfile
# │ └── app.py
# ├── docker-compose.yml
# └── README.md


# =============================================
# =============================================
# 💡 Cách chạy toàn hệ thống
# =============================================
# 1️⃣ Cài Docker Desktop hoặc Docker Engine
# 2️⃣ Lưu toàn bộ cấu trúc trên
# 3️⃣ Mở terminal: docker-compose up --build
# 4️⃣ Kiểm tra các endpoint:
#     - http://localhost:5001/api/users
#     - http://localhost:5002/api/orders
#     - http://localhost:5003/api/products
#     - http://localhost:5003/api/suggest
#     - Kibana: http://localhost:5601
#     - RabbitMQ: http://localhost:15672
# 5️⃣ Mọi thứ sẽ tự container hóa và hoạt động đồng bộ.
# =============================================