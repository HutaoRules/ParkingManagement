from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import NguoiDung, KhachHang, NhanVien, TaiKhoan
#import database
from app import db
from flask import Flask, request, jsonify


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('first.html')

from werkzeug.security import generate_password_hash
from datetime import datetime
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        tenDangNhap = request.form.get('tenDangNhap')
        matKhau = request.form.get('matKhau')
        confirmPassword = request.form.get('confirm-password')
        email = request.form.get('email')
        hoTen = request.form.get('hoTen')
        SDT = request.form.get('SDT')
        vaiTro = 'customer'

        # Basic validation
        if not all([tenDangNhap, matKhau, email, hoTen, SDT]):
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return redirect(url_for('auth.register'))

        if matKhau != confirmPassword:
            flash('Mật khẩu xác nhận không khớp', 'error')
            return redirect(url_for('auth.register'))

        try:
            # First, create the TaiKhoan
            taikhoan = TaiKhoan(
                tenDangNhap=tenDangNhap,
                matKhau=matKhau,
                email=email,
                ngayTaoTaiKhoan=datetime.utcnow()
            )
            db.session.add(taikhoan)
            
            # Create KhachHang directly (this will automatically create the nguoidung entry due to inheritance)
            khachhang = KhachHang(
                maKH=tenDangNhap,  # This will also set maND due to inheritance
                maND=tenDangNhap,  # Explicitly set maND
                email=email,
                hoTen=hoTen,
                SDT=SDT,
                vaiTro=vaiTro,
                soDu=0
            )
            db.session.add(khachhang)

            # Commit the transaction
            db.session.commit()
            return redirect(url_for('auth.identify'))

        except IntegrityError as e:
            db.session.rollback()
            print(f"Database integrity error: {str(e)}")
            return redirect(url_for('auth.register'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth_bp.route('/identify')
def identify():
    return render_template('login.html')

# Constants for role types
VALID_ROLES = {'customer', 'staff', 'manager'}
ROLE_REDIRECTS = {
    'customer': 'customer.index',
    'staff': 'staff.dashboard',
    'manager': 'manager.dashboard'
}



@auth_bp.route('/login/<string:type>', methods=['GET', 'POST'])
def login(type):
    # Validate role type
    if type not in VALID_ROLES:
        return redirect(url_for('auth.login', type='customer'))

    if request.method == 'POST':
        identifier = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Basic input validation
        if not identifier or not password:
            flash('Vui lòng nhập đầy đủ thông tin đăng nhập', 'error')
            return render_template('login_type.html', type=type)

        try:
            # First try to find user by email
            user = TaiKhoan.query.filter_by(tenDangNhap=identifier).first()
            if not user:
                # If not found by email, try username
                user = TaiKhoan.query.filter_by(tenDangNhap=identifier).first()

            if not user:
                flash('Tài khoản không tồn tại', 'error')
                return render_template('login_type.html', type=type)

            # Check password (assuming you're using werkzeug's password hashing)
            if user.matKhau != password:
                flash('Mật khẩu không đúng', 'error')
                return render_template('login_type.html', type=type)

            # Check user role
            nguoidung = NguoiDung.query.filter_by(
                maND=user.tenDangNhap,
                vaiTro=type
            ).first()

            if not nguoidung:
                flash(f'Tài khoản của bạn không có quyền truy cập vào khu vực này', 'error')
                return render_template('login_type.html', type=type)

            # Set session data
            session.clear()  # Clear any existing session
            session['user'] = nguoidung.maND
            session['type'] = type
            session['email'] = user.email
            session['hoTen'] = nguoidung.hoTen

            # Optional: Add last login timestamp
            try:
                user.last_login = datetime.utcnow()
                db.session.commit()
            except:
                db.session.rollback()  # Don't let this stop the login process
            
            # Redirect based on role
            return redirect(url_for(ROLE_REDIRECTS[type]))

        except Exception as e:
            # Log the error for debugging
            print(f"Login error: {str(e)}")
            flash('Có lỗi xảy ra. Vui lòng thử lại sau.', 'error')
            return render_template('login_type.html', type=type)

    # GET request
    return render_template('login_type.html', type=type)