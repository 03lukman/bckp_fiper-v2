from flask import Blueprint, render_template, request, redirect, url_for, session, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    # Jika user sudah login, jangan tampilkan form login lagi, langsung lempar ke dashboard
    if session.get('logged_in'):
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin_user = current_app.config['ADMIN_USER']
        admin_pass = current_app.config['ADMIN_PASS']

        if username == admin_user and password == admin_pass:
            # Session permanen agar login tidak cepat habis (opsional)
            session.permanent = True 
            session['logged_in'] = True
            return redirect(url_for('dashboard.index'))
        
        # Gunakan error handling yang lebih informatif
        return render_template('auth/login.html', error="Kredensial tidak valid.")

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear() # Menghapus semua data session
    return redirect(url_for('auth.login'))