from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import NguoiDung, KhachHang, NhanVien

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('login.html')

@auth_bp.route('/login/<string:type>', methods=['GET', 'POST'])
def login(type):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if type == 'customer':
            user = KhachHang.query.filter_by(Email=email, MatKhau=password).first()
        elif type == 'staff':
            user = NhanVien.query.filter_by(Email=email, MatKhau=password).first()
        elif type == 'manager':
            user = NguoiDung.query.filter_by(Email=email, MatKhau=password).first()

        if user:
            session['user'] = user.MaND
            session['type'] = type
            return redirect(url_for('auth.index'))
        else:
            flash('Email hoặc mật khẩu không đúng')
    return render_template('login_type.html')