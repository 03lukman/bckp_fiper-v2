from flask import Blueprint, render_template, jsonify, session, redirect, request, url_for, current_app
from app.modules.auth.helpers import login_required
import json
import os

dashboard_bp = Blueprint('dashboard', __name__)
LOG_FILE = "activity_logs.json"

@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Pastikan jika session kosong, kita set default
    if 'active_db' not in session:
        session['active_db'] = 'DUNIABARU'
    return render_template('dashboard/index.html')

@dashboard_bp.route('/set_database/<db_alias>')
@login_required
def set_database(db_alias):
    """Update database aktif di session berdasarkan pilihan Navbar"""
    db_configs = current_app.config.get('DATABASES', {})
    
    if db_alias in db_configs:
        session['active_db'] = db_alias
    
    # Ambil URL sebelumnya atau kembali ke dashboard
    next_page = request.args.get('next') or url_for('dashboard.index')
    return redirect(next_page)

@dashboard_bp.route('/get_logs')
@login_required
def get_logs():
    """Mengambil 20 log aktivitas terbaru"""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
            return jsonify(logs[:20])
        except (json.JSONDecodeError, IOError):
            return jsonify([])
    return jsonify([])