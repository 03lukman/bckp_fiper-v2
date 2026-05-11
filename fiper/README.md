# FINA Report System Automation

Sistem otomatisasi berbasis web untuk mengekstrak data laporan dari database FINA (Firebird) dan mengonversinya ke format Excel. Sistem ini dilengkapi dengan fitur dashboard pemantauan real-time dan containerization menggunakan Docker.

## 🚀 Fitur Utama

- **Ekstraksi Data Otomatis**: Menarik data Piutang AR, Faktur Lengkap, Register SO, dan DO Pengiriman langsung dari database Firebird FINA.
- **Preview & Filter**: Menampilkan data di web sebelum diunduh untuk memastikan akurasi (misal: Preview Register SO).
- **Format Excel Professional**: Mengotomatisasi pembuatan laporan Excel dengan fitur *Auto-fit columns* agar siap digunakan.
- **Dashboard Web**: Antarmuka berbasis Flask untuk memilih sumber database (Pusat, Matraman, Surabaya, dll.) dan jenis laporan.
- **Sistem Log Real-time**: Mencatat aktivitas IP pengguna, waktu, dan jenis tindakan (Download/Email) secara transparan di dashboard.
- **Integrasi Email & WhatsApp**: Mengirimkan ringkasan laporan Register SO langsung melalui email dengan format tabel HTML atau teks ringkasan untuk WhatsApp.
- **Containerization**: Dideploy menggunakan Docker untuk konsistensi environment dan kemudahan manajemen sistem.

## 🛠️ Stack Teknologi

- **Bahasa Pemrograman**: Python 3.x
- **Database**: Firebird SQL (menggunakan library `firebirdsql` / `fdb`)
- **Web Framework**: Flask
- **Data Processing**: Pandas, Openpyxl
- **Deployment**: Docker & Docker Compose
- **Networking**: Tailscale (Untuk koneksi site-to-site antar kantor Matraman, Salembaran, Surabaya, dan Bantargebang)

## 📁 Struktur Proyek

- `app.py` / `piutang.py`: Logic utama aplikasi, routing Flask, dan query database.
- `templates/`: Folder berisi file HTML (Dashboard utama, Preview SO, Preview Piutang).
- `logs/`: Penyimpanan file log aktivitas sistem (`activity.log`).
- `Dockerfile` & `docker-compose.yml`: Konfigurasi untuk deploy container.

## ⚙️ Cara Instalasi & Penggunaan

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>