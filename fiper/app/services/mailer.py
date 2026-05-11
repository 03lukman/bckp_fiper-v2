import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import current_app

class MailerService:
    def __init__(self):
        # Daftar group tetap dipertahankan untuk kemudahan operasional
        self.groups = {
            "pabrik": [
                "ifan@in.agson.co.id",
                "anang@in.agson.co.id",
                "rodin@in.agson.co.id",
                "jalal@in.agson.co.id"
            ],
            "office": ["admin@agson.co.id", "finance@agson.co.id"]
        }

    def send_report(self, to_input, subject, table_html, note, attachment_data, db_name):
        smtp_server = current_app.config.get('MAIL_SERVER')
        smtp_port = current_app.config.get('MAIL_PORT')
        sender_email = current_app.config.get('MAIL_USERNAME')
        sender_password = current_app.config.get('MAIL_PASSWORD')

        target_emails = self.groups.get(to_input.lower(), [to_input])
        
        msg = MIMEMultipart()
        msg['From'] = f"FINA Helper System <{sender_email}>"
        msg['To'] = ", ".join(target_emails)
        msg['Subject'] = subject

        # --- LOGIKA STYLING TABEL LEBAR & OTOMATIS RATA KANAN (ANGKA) ---
        
        # 1. Setup Table Base (Font 12px & Width Lega)
        styled_table = table_html.replace(
            '<table border="1" class="dataframe table">', 
            '<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; border: 1px solid black; font-size: 12px;">'
        )

        # 2. Styling Header (Tetap Center & Background Gelap)
        styled_table = styled_table.replace(
            '<th>', 
            '<th style="background-color: #212529; color: white; border: 1px solid black; padding: 10px; text-align: center; white-space: nowrap;">'
        )

        # 3. Logika Rata Kanan Otomatis (Regex)
        # Fungsi ini mencari tag <td>, jika isinya angka/qty, maka align right.
        def align_cells(match):
            content = match.group(1)
            # Cek apakah konten adalah angka (mendukung angka negatif, koma, dan titik)
            if re.match(r'^-?\d+([.,]\d+)?$', content.strip()):
                return f'<td style="border: 1px solid black; padding: 8px; text-align: right; font-weight: bold;">{content}</td>'
            else:
                return f'<td style="border: 1px solid black; padding: 8px; text-align: left;">{content}</td>'

        # Eksekusi penggantian tag <td> standar dengan tag yang sudah di-align
        styled_table = re.sub(r'<td>(.*?)</td>', align_cells, styled_table)

        body_html = f"""
        <html>
          <body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 20px;">
            <div style="max-width: 1100px; margin: auto; border: 1px solid #ddd; padding: 25px; background-color: #ffffff; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                <h2 style="color: #0d6efd; border-bottom: 2px solid #0d6efd; padding-bottom: 10px; margin-top: 0;">
                    Laporan Register SO
                </h2>
                <p>Halo Team,</p>
                <p>Berikut adalah rincian data yang diekstrak dari Database: <b style="color: #d63384;">{db_name}</b></p>
                
                <div style="margin-top: 20px; margin-bottom: 20px; overflow-x: auto;">
                    {styled_table}
                </div>
                
                <div style="background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; margin-top: 20px;">
                    <p style="margin: 0; font-weight: bold; color: #856404; font-size: 14px;">Catatan Tambahan:</p>
                    <p style="margin: 5px 0 0 0; font-size: 24px; color: #000; font-weight: bold;">{note}</p>
                </div>
                
                <p style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 15px; font-size: 11px; color: #888; text-align: center;">
                    Email ini dikirim otomatis oleh <strong>Sistem Otomasi Laporan FINA v2</strong><br>
                    IT ADMINISTRATOR - AGSON INTERNATIONAL
                </p>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(body_html, 'html'))

        # Lampiran Excel
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=Register_SO_{db_name}.xlsx')
        msg.attach(part)

        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            return True, "Email berhasil dikirim!"
        except Exception as e:
            return False, str(e)

mailer_service = MailerService()