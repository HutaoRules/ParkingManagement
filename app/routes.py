from flask import render_template, request, redirect, url_for
from app import app
from app.models import NguoiDung, KhachHang, NhanVien, Xe, LoaiVe, Ve
from app import db
from datetime import datetime
from flask import session

@app.route('/', methods=['GET', 'POST'])

    
@app.route('/trangchukhachhang')
def trangchukhachhang():
    user = KhachHang.query.filter_by(MaKH= session['MaND']).first()
    return render_template('trangchukhachhang.html', user=user)

@app.route('/trangchunhanvien')
def trangchunhanvien():
    User = NhanVien.query.filter_by(MaNV= session['MaND']).where(NhanVien.ViTriNhanVien == 'NhanVien').first()
    return render_template('trangchunhanvien.html', user=User)

@app.route('/trangchuquanly')
def trangchuquanly():
    User = NhanVien.query.filter_by(MaND= session['MaND']).where(NhanVien.ViTriNhanVien == 'QuanLy').first()
    return render_template('trangchuquanly.html', user=User)
