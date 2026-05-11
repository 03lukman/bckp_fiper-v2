import os
from dotenv import load_dotenv

# Memuat file .env dari root folder
load_dotenv()

class Config:
    # Flask Core
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fina_secret_key')
    
    # Auth
    ADMIN_USER = os.environ.get('ADMIN_USER')
    ADMIN_PASS = os.environ.get('ADMIN_PASS')
    
    # Mail Config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Database Map (Sudah Mendukung Port & Charset dari .env)
    DATABASES = {
        'DUNIABARU': {
            'host': os.environ.get('DB_HOST_PUSAT'),
            'port': int(os.environ.get('DB_PORT_PUSAT') or 3051),
            'path': os.environ.get('DB_PATH_PUSAT'),
            'user': os.environ.get('DB_USER_PUSAT'),
            'password': os.environ.get('DB_PASS_PUSAT'),
            'charset': os.environ.get('DB_CHARSET_PUSAT', 'WIN1252')
        },
        'SURABAYA': {
            'host': os.environ.get('DB_HOST_SBY'),
            'port': int(os.environ.get('DB_PORT_SBY') or 3051),
            'path': os.environ.get('DB_PATH_SBY'),
            'user': os.environ.get('DB_USER_SBY'),
            'password': os.environ.get('DB_PASS_SBY'),
            'charset': os.environ.get('DB_CHARSET_SBY', 'WIN1252')
        }
    }

    