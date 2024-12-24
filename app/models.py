from app import db
from datetime import datetime

# Models
class TaiKhoan(db.Model):
    __tablename__ = 'taikhoan'
    tenDangNhap = db.Column(db.String(50), primary_key=True)
    matKhau = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    ngayTaoTaiKhoan = db.Column(db.Date, default=datetime.utcnow)


class NguoiDung(db.Model):
    __tablename__ = 'nguoidung'
    maND = db.Column(db.String(25), primary_key=True)
    email = db.Column(db.String(100), db.ForeignKey('taikhoan.email'), unique=True, nullable=False)
    hoTen = db.Column(db.String(50), nullable=False)
    SDT = db.Column(db.String(15), nullable=False)
    vaiTro = db.Column(db.String(10), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'nguoidung',
        'polymorphic_on': vaiTro
    }

class NhanVien(NguoiDung):
    __tablename__ = 'nhanvien'
    maNV = db.Column(db.String(25), db.ForeignKey('nguoidung.maND'), primary_key=True)
    viTriNhanVien = db.Column(db.String(30), nullable=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff'  # Added this line
    }



class KhachHang(NguoiDung):
    __tablename__ = 'khachhang'
    maKH = db.Column(db.String(25), db.ForeignKey('nguoidung.maND'), primary_key=True)
    soDu = db.Column(db.Numeric, default=0)
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }
class KhachVangLai(db.Model):
    __tablename__ = 'khachvanglai'
    maTheKVL = db.Column(db.String(25), primary_key=True)
    maXe = db.Column(db.String(25), db.ForeignKey('xe.maXe'))
    hoTen = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    SDT = db.Column(db.String(15), nullable=True)


class Xe(db.Model):
    __tablename__ = 'xe'
    maXe = db.Column(db.String(25), primary_key=True)
    bienSoXe = db.Column(db.String(20), unique=True, nullable=False)
    loaiXe = db.Column(db.String(20), nullable=False)


class LoaiVe(db.Model):
    __tablename__ = 'loaive'
    maLoaiVe = db.Column(db.String(25), primary_key=True)
    tenLoaiVe = db.Column(db.String(20), nullable=False)
    giaVe = db.Column(db.Numeric, nullable=False)
    
    def to_dict(self):
        return {
            'maLoaiVe': self.maLoaiVe,
            'tenLoaiVe': self.tenLoaiVe,
            'giaVe': str(self.giaVe)  # Chuyển giaVe thành chuỗi
        }

class Ve(db.Model):
    __tablename__ = 've'
    maVe = db.Column(db.String(25), primary_key=True)
    maLoaiVe = db.Column(db.String(25), db.ForeignKey('loaive.maLoaiVe'))
    maKH = db.Column(db.String(25), db.ForeignKey('khachhang.maKH'))
    trangThaiSD = db.Column(db.Boolean, default=False)
    ngayKichHoat = db.Column(db.DateTime, nullable=True)
    ngayHetHan = db.Column(db.DateTime, nullable=True)


class HoaDonMuaVe(db.Model):
    __tablename__ = 'hoadonmuave'
    maHD = db.Column(db.String(25), primary_key=True)
    maKH = db.Column(db.String(25), db.ForeignKey('khachhang.maKH'))
    ngayHD = db.Column(db.DateTime, default=datetime.utcnow)
    tongTriGia = db.Column(db.Numeric, nullable=False)


class ChiTietHoaDonMuaVe(db.Model):
    __tablename__ = 'chitiethoadonmuave'
    maHD = db.Column(db.String(25), db.ForeignKey('hoadonmuave.maHD'), primary_key=True)
    maLoaiVe = db.Column(db.String(25), db.ForeignKey('loaive.maLoaiVe'), primary_key=True)
    soLuongVe = db.Column(db.Numeric, nullable=False)


class ChiTietVaoRa(db.Model):
    __tablename__ = 'chitietvaora'
    maCTVR = db.Column(db.String(25), primary_key=True)
    maTheKVL = db.Column(db.String(25), db.ForeignKey('khachvanglai.maTheKVL'))
    maXe = db.Column(db.String(25), db.ForeignKey('xe.maXe'))
    thoiGianVao = db.Column(db.DateTime, nullable=False)
    thoiGianRa = db.Column(db.DateTime, nullable=True)