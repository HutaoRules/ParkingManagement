from app import db

#Class Nguoi Dung
class NguoiDung(db.Model):
    __tablename__ = 'NguoiDung'
    MaND = db.Column(db.String(5), primary_key=True)
    Email = db.Column(db.String(50), nullable=False)
    MatKhau = db.Column(db.String(50), nullable=False)
    HoTen = db.Column(db.String(50), nullable=False)
    GioiTinh = db.Column(db.String(3), nullable=False)
    NgSinh = db.Column(db.Date, nullable=False)
    DiaChi = db.Column(db.String(100), nullable=True)
    QueQuan = db.Column(db.String(50), nullable=True)
    SDT = db.Column(db.String(10), nullable=False)

    type = db.Column(db.String(20))
    __mapper_args__ = {
        'polymorphic_identity':'NguoiDung',
        'polymorphic_on':type
    }

#Class Xe
class Xe(db.Model):
    __tablename__ = 'Xe'
    MaXe = db.Column(db.String(5), primary_key=True)
    BienSoXe = db.Column(db.String(30), nullable=False)
    TenLoaiXe = db.Column(db.String(20), nullable=True)

#Class LoaiVe
class LoaiVe(db.Model):
    __tablename__ = 'LoaiVe'
    MaLoaiVe = db.Column(db.String(5), primary_key=True)
    TenLoaiVe = db.Column(db.String(20), nullable=False)
    GiaVe = db.Column(db.Float, nullable=False)

#class khach hang la lop con cua lop NguoiDung
class KhachHang(NguoiDung):
    __tablename__ = 'KhachHang'
    MaKH = db.Column(db.String(5), db.ForeignKey('NguoiDung.MaND'), primary_key=True)
    MaXe = db.Column(db.String(5), db.ForeignKey('Xe.MaXe'), nullable=False)
    SoDu = db.Column(db.Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'KhachHang'
    }

#class nhan vien la lop con cua lop NguoiDung
class NhanVien(NguoiDung):
    __tablename__ = 'NhanVien'
    MaNV = db.Column(db.String(5), db.ForeignKey('NguoiDung.MaND'), primary_key=True)
    ViTriNhanVien = db.Column(db.String(30), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'NhanVien'
    }

#class Ve 
class Ve(db.Model):
    __tablename__ = 'Ve'
    MaVe = db.Column(db.String(5), primary_key=True)
    MaLoaiVe = db.Column(db.String(5), db.ForeignKey('LoaiVe.MaLoaiVe'), nullable=False)
    MaKH = db.Column(db.String(5), db.ForeignKey('KhachHang.MaKH'), nullable=False)
    NgayKichHoat = db.Column(db.Date, nullable=False)
    NgayHetHan = db.Column(db.Date, nullable=False)
    TrangThai = db.Column(db.String(30), nullable=False)

#class KhachHangVangLai
class KhachVangLai(db.Model):
    __tablename__ = 'KhachVangLai'
    MaTheKVL = db.Column(db.String(5), primary_key=True)
    MaXe = db.Column(db.String(5), db.ForeignKey('Xe.MaXe'), nullable=False)

#class Phan Hoa Don va Bao cao
class ChiTietRaVao(db.Model):
    __tablename__ = 'ChiTietRaVao'
    MaCTRV = db.Column(db.String(5), primary_key=True)
    MaTheKVL = db.Column(db.String(5), db.ForeignKey('KhachVangLai.MaTheKVL'), nullable=False)
    MaXe = db.Column(db.String(5), db.ForeignKey('Xe.MaXe'), nullable=False)
    MaKH = db.Column(db.String(5), db.ForeignKey('KhachHang.MaKH'), nullable=False)
    ThoiGianVao = db.Column(db.DateTime, nullable=False)
    ThoiGianRa = db.Column(db.DateTime, nullable=False)

class HoaDonMuaVe(db.Model):
    __tablename__ = 'HoaDonMuaVe'
    MaHD = db.Column(db.String(5), primary_key=True)
    MaKH = db.Column(db.String(5), db.ForeignKey('KhachHang.MaKH'), nullable=False)
    NgayHD = db.Column(db.Date, nullable=False)
    TongTien = db.Column(db.Float, nullable=False)

class ChiTietHoaDon(db.Model):
    __tablename__ = 'ChiTietHoaDon'
    MaHD = db.Column(db.String(5), db.ForeignKey('HoaDonMuaVe.MaHD'), primary_key=True, nullable=False)
    MaVe = db.Column(db.String(5), db.ForeignKey('Ve.MaVe'), primary_key=True, nullable=False)
    SoLuongVe = db.Column(db.Integer, nullable=False)
