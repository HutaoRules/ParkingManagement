from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import NguoiDung, KhachHang, NhanVien, Ve, Xe, LoaiVe, KhachVangLai
from app import db
from datetime import datetime
import random
import string


customer_bp = Blueprint('customer', __name__)

Cart = []

@customer_bp.route('/index')
def index():
    user_id = session['user']
    user = NguoiDung.query.filter_by(maND=user_id).first()
    customer = KhachHang.query.filter_by(maND=user_id).first()
    return render_template('index.html', user=user, customer=customer)

@customer_bp.route('/logout')
def logout():
    session.pop('user')
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.identify'))

@customer_bp.route('/buy_ticket', methods=['GET', 'POST'])
def buy_ticket():
    global Cart
    user_id = session.get('user')
    
    # Kiểm tra xem người dùng đã đăng nhập hay chưa
    if not user_id:
        return redirect(url_for('customer.login'))  # Nếu chưa đăng nhập thì chuyển hướng tới trang login

    # Lấy thông tin người dùng
    user = NguoiDung.query.filter_by(maND=user_id).first()
    customer = KhachHang.query.filter_by(maND=user_id).first()
    tickets = LoaiVe.query.all()

    # Xử lý nếu có yêu cầu POST
    if request.method == 'POST':
        # Lấy dữ liệu giỏ hàng từ request
        data = request.get_json()
        tickets = data.get('tickets', [])
        for ticket in tickets:
            ticketName = ticket.split(' - ')[0]
            loaive = LoaiVe.query.filter_by(tenLoaiVe=ticketName).first()
        # Lưu giỏ hàng vào session (hoặc bạn có thể lưu vào cơ sở dữ liệu nếu muốn)
            Cart.append(loaive)
        
        # Trả về phản hồi cho client
        return jsonify({'status': 'success', 'message': 'Vé đã được thêm vào giỏ hàng!', 'cart': tickets})
    return render_template('buyticket.html', user=user, customer=customer, tickets = tickets)

@customer_bp.route('/deposit', methods=['GET', 'POST'])
def deposit():
    user_id = session['user']
    user = NguoiDung.query.filter_by(maND=user_id).first()
    customer = KhachHang.query.filter_by(maND=user_id).first()

    if request.method == 'POST':
        amount = request.form['amount']
        # Convert the amount (string) to an integer (removing commas)
        amount = int(amount.replace(",", ""))
        # Add the amount to the customer's balance
        customer.soDu += amount  # Adjust according to your data model
        db.session.commit()
        flash("Nạp tiền thành công!", "success")
        return redirect(url_for('customer.deposit'))

    return render_template('deposit.html', user=user, customer=customer)
@customer_bp.route('/ticketdetail')
def ticketdetail():
    user_id = session['user']
    user = NguoiDung.query.filter_by(maND=user_id).first()
    customer = KhachHang.query.filter_by(maND=user_id).first()
    return render_template('ticketdetail.html', user=user, customer=customer)

@customer_bp.route('/cart')
def cart():
    user_id = session['user']
    user = NguoiDung.query.filter_by(maND=user_id).first()
    customer = KhachHang.query.filter_by(maND=user_id).first()

    cart_items = [ item.to_dict() for item in Cart ]
    return render_template('cart.html', user=user, customer=customer, cart=cart_items)

@customer_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    global Cart
    item_name = request.json.get('item')
    cart = Cart

    # Loại bỏ item khỏi cart
    cart = [item for item in cart if not item.startswith(item_name)]
    Cart = cart

    return jsonify({'success': True})

# @customer_bp.route('cart/checkout', methods=['POST'])
# def checkout():
#     global Cart
#     Cart = []  # Xóa giỏ hàng sau khi thanh toán
#     return jsonify({'success': True})