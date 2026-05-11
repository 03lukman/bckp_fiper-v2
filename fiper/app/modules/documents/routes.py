from flask import Blueprint, render_template, request, jsonify, send_file, session
from app.modules.auth.helpers import login_required
from app.services.database import db_service
from app.services.logger_service import logger_service
from app.services.mailer import mailer_service
from app.services.document_service import doc_service
from .queries import QUERY_PIUTANG, QUERY_SO, QUERY_DO, QUERY_FAKTUR
from datetime import datetime
import pandas as pd
import io

documents_bp = Blueprint('documents', __name__)

# --- INTERNAL HELPER UNTUK DOWNLOAD ---
def _send_excel_response(json_data, db_name, sheet_name, prefix):
    output = doc_service.generate_excel_file(json_data, sheet_name)
    if not output:
        return "Data tidak valid", 400
    
    logger_service.log_action(f"Download {prefix}", db_name)
    
    filename = f"{prefix}_{db_name}_{datetime.now().strftime('%Y%m%d')}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# ==========================================
# 1. ROUTES PREVIEW (Menggunakan Global Session)
# ==========================================

@documents_bp.route('/preview/piutang')
@login_required
def preview_piutang():
    db = session.get('active_db', 'DUNIABARU')
    df = db_service.execute_query(db, QUERY_PIUTANG)
    df = doc_service.format_dataframe(df, date_cols=['TANGGAL', 'JATUH_TEMPO'], num_cols=['NOMINAL_INV'])
    return render_template('documents/preview_piutang.html', data=df.to_dict(orient='records'), db=db)

@documents_bp.route('/preview/register_so')
@login_required
def preview_so():
    db = session.get('active_db', 'DUNIABARU')
    df = db_service.execute_query(db, QUERY_SO)
    df = doc_service.format_dataframe(df, date_cols=['TANGGAL_SO'], num_cols=['QTY'])
    return render_template('documents/preview_so.html', data=df.to_dict(orient='records'), db=db)

@documents_bp.route('/preview/do_pengiriman')
@login_required
def preview_do():
    db = session.get('active_db', 'DUNIABARU')
    df = db_service.execute_query(db, QUERY_DO)
    df = doc_service.format_dataframe(df, date_cols=['TANGGAL_SJ'], num_cols=['QTY'])
    return render_template('documents/preview_do.html', data=df.to_dict(orient='records'), db=db, now=datetime.now().strftime('%d/%m/%Y %H:%M'))

@documents_bp.route('/preview/faktur')
@login_required
def preview_faktur():
    db = session.get('active_db', 'DUNIABARU')
    df = db_service.execute_query(db, QUERY_FAKTUR)
    df = doc_service.format_dataframe(df, date_cols=['Tgl Faktur'], num_cols=['Kts', 'Harga Satuan', 'DPP', 'PPN', 'Total Faktur'])
    return render_template('documents/preview_faktur.html', data=df.to_dict(orient='records'), db=db)

# ==========================================
# 2. ROUTES DOWNLOAD
# ==========================================

@documents_bp.route('/download/selected_piutang', methods=['POST'])
@login_required
def download_piutang():
    return _send_excel_response(request.form.get('selected_rows'), request.form.get('db'), 'Piutang', 'Piutang_AR')

@documents_bp.route('/download/selected_so', methods=['POST'])
@login_required
def download_so():
    return _send_excel_response(request.form.get('selected_rows'), request.form.get('db'), 'RegisterSO', 'Register_SO')

@documents_bp.route('/download/selected_do', methods=['POST'])
@login_required
def download_do():
    return _send_excel_response(request.form.get('selected_rows'), request.form.get('db'), 'DOPengiriman', 'DO_Pengiriman')

@documents_bp.route('/download/selected_faktur', methods=['POST'])
@login_required
def download_faktur():
    return _send_excel_response(request.form.get('selected_rows'), request.form.get('db'), 'FakturLengkap', 'Faktur_Lengkap')

# ==========================================
# 3. MAILER ROUTES
# ==========================================

@documents_bp.route('/send_email_so', methods=['POST'])
@login_required
def send_email_so():
    try:
        req_data = request.get_json()
        target_input, db_name, rows = req_data.get('email'), req_data.get('db'), req_data.get('data')
        note = req_data.get('note', '-')

        if not target_input or not rows:
            return jsonify({"message": "Data tidak lengkap!"}), 400

        df = pd.DataFrame(rows)
        table_html = df.to_html(index=False, classes='table', border=1, justify='left')
        excel_output = doc_service.generate_excel_file(rows, 'RegisterSO')

        success, message = mailer_service.send_report(
            to_input=target_input,
            subject=f"Laporan Register SO - {db_name}",
            table_html=table_html,
            note=note,
            attachment_data=excel_output.getvalue(),
            db_name=db_name
        )

        if success:
            logger_service.log_action(f"Email SO ke {target_input}", db_name)
            return jsonify({"message": f"Email berhasil dikirim ke {target_input}!"}), 200
        return jsonify({"message": f"Gagal: {message}"}), 500

    except Exception as e:
        return jsonify({"message": str(e)}), 500