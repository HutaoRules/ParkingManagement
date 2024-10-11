from app import create_app, db
from app.models import NguoiDung, Xe, LoaiVe, KhachHang, NhanVien, Ve

app = create_app()

with app.app_context():
    db.create_all()
    db.session.commit()
    print('Database created!')