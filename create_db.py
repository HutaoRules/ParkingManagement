from app import create_app, db
from app.models import NguoiDung, Xe, LoaiVe, KhachHang, NhanVien, Ve

def create_db():
    app = create_app()
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
# Compare this snippet from app/blueprints/login.py:
