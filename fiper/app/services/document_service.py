# app/services/document_service.py
import pandas as pd
import io
import json
from openpyxl.styles import Font
from datetime import datetime

class DocumentService:
    @staticmethod
    def format_dataframe(df, date_cols=None, num_cols=None):
        """Membersihkan dan memformat data untuk tampilan HTML"""
        if df.empty:
            return df
        
        if date_cols:
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%d/%m/%Y')
        
        if num_cols:
            for col in num_cols:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: "{:,.0f}".format(x) if pd.notnull(x) else "0")
        return df

    @staticmethod
    def generate_excel_file(json_data, sheet_name):
        """Mengolah data JSON menjadi file Excel siap kirim/download"""
        if not json_data:
            return None
        
        rows = json.loads(json_data) if isinstance(json_data, str) else json_data
        df = pd.DataFrame(rows)
        
        # Kolom-kolom yang harus dikembalikan ke angka agar Excel bisa menjumlahkan
        target_cols = ['Kts', 'Total Faktur', 'QTY', 'DPP', 'PPN', 'Harga Satuan', 'Disk%', 'NOMINAL_INV']
        for col in target_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            ws = writer.sheets[sheet_name]

            # Logika Autofit Kolom
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except: pass
                ws.column_dimensions[column_letter].width = max_length + 2
                ws.cell(row=1, column=column[0].column).font = Font(bold=True)

        output.seek(0)
        return output

doc_service = DocumentService()