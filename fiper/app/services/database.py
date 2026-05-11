import firebirdsql
import pandas as pd
from flask import current_app

class DatabaseService:
    def get_connection(self, db_alias):
        """
        Membangun koneksi ke Firebird secara dinamis berdasarkan alias.
        Semua parameter diambil dari Config (hasil pembacaan .env).
        """
        db_configs = current_app.config.get('DATABASES')
        
        if not db_configs:
            raise ValueError("Konfigurasi DATABASES tidak ditemukan!")

        config = db_configs.get(db_alias)
        
        if not config:
            raise ValueError(f"Database alias '{db_alias}' tidak terdaftar!")

        # Koneksi bersih menggunakan variabel dari .env
        return firebirdsql.connect(
            host=config['host'],
            port=config['port'],
            database=config['path'],
            user=config['user'],
            password=config['password'],
            charset=config['charset']
        )

    def execute_query(self, db_alias, query):
        """
        Eksekusi query SQL dan return sebagai DataFrame.
        Dilengkapi Trimming kolom agar sinkron dengan template HTML.
        """
        conn = None
        try:
            conn = self.get_connection(db_alias)
            df = pd.read_sql(query, conn)
            
            # Membersihkan spasi pada nama kolom (Penting untuk Firebird)
            df.columns = [col.strip() for col in df.columns]
            
            return df
            
        except Exception as e:
            # Tetap simpan log error di terminal jika terjadi masalah jaringan mendadak
            print(f"--- DATABASE ERROR [{db_alias}] ---")
            print(f"Detail: {e}")
            return pd.DataFrame()
            
        finally:
            if conn:
                conn.close()

# Singleton instance
db_service = DatabaseService()