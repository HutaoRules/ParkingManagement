from models import NguoiDung, KhachHang, NhanVien, Ve, Xe, LoaiVe, KhachVangLai

class TaiKhoan:
    def __init__(self, ten, matkhau):
        self.ten = ten
        self.matkhau = matkhau

    def __str__(self):
        return f"{self.ten} - {self.matkhau}"