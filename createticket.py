from app import db  # Đảm bảo đã import `db` từ ứng dụng của bạn
from app.models import LoaiVe  # Import class LoaiVe từ file models của bạn
from app import create_app, db
from app.models import NguoiDung, Xe, LoaiVe, KhachHang, NhanVien, Ve

def seed_loai_ve():
    # Dữ liệu loại vé
    loai_ve_data = [
        {'maLoaiVe': 'VE_THANG', 'tenLoaiVe': 'Vé tháng', 'giaVe': 70000},
        {'maLoaiVe': 'XE_MAY', 'tenLoaiVe': 'Xe máy', 'giaVe': 3000},
        {'maLoaiVe': 'XE_DAP', 'tenLoaiVe': 'Xe đạp', 'giaVe': 2000},
        {'maLoaiVe': 'Ve_TUAN', 'tenLoaiVe': 'Vé tuần', 'giaVe': 30000}
        ]

    # Thêm từng loại vé vào cơ sở dữ liệu
    for ve in loai_ve_data:
        new_ve = LoaiVe(
            maLoaiVe=ve['maLoaiVe'],
            tenLoaiVe=ve['tenLoaiVe'],
            giaVe=ve['giaVe']
        )
        db.session.add(new_ve)

    # Lưu thay đổi vào cơ sở dữ liệu
    try:
        db.session.commit()
        print("Thêm loại vé thành công!")
    except Exception as e:
        db.session.rollback()
        print("Có lỗi xảy ra:", e)

if __name__ == '__main__':
    app = create_app()  # Tạo app Flask từ hàm create_app
    with app.app_context():  # Kích hoạt application context
        seed_loai_ve()