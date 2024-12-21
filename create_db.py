from app import create_app, db
from app.models import NguoiDung, Xe, LoaiVe, KhachHang, NhanVien, Ve

def create_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.add(NguoiDung(MaND='ND001', Email = 'dotuan@gmail.hust', MatKhau = '123456', HoTen = 'Do Tuan', GioiTinh = 'Nam', NgSinh = '1999-10-10', DiaChi = 'Ha Noi', QueQuan = 'Ha Noi', SDT = '0123456789', VaiTro = 'KhachHang'))
        db.session.commit()

if __name__ == '__main__':
    create_db()
# Compare this snippet from app/blueprints/login.py:
