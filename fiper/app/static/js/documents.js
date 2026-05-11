/**
 * FINA Helper - Global Document Services
 * Logic for Filtering, Downloading, and Emailing Reports
 * Optimized for Enterprise UX with Toast Notifications
 */

let emailBootstrapModal;

// Inisialisasi komponen Bootstrap saat halaman selesai dimuat
document.addEventListener('DOMContentLoaded', function() {
    const modalEl = document.getElementById('emailModal');
    if (modalEl) {
        emailBootstrapModal = new bootstrap.Modal(modalEl);
    }
});

/**
 * HELPER: NOTIFIKASI TOAST (MODERN & NON-BLOCKING)
 * @param {string} message - Pesan yang ingin ditampilkan
 * @param {string} type - 'success' (hijau) atau 'danger' (merah)
 */
function showToast(message, type = 'success') {
    const toastEl = document.getElementById('liveToast');
    const toastBody = document.getElementById('toastMessage');
    
    if (!toastEl || !toastBody) return; // Guard clause jika elemen tidak ditemukan

    // Reset & Set warna background berdasarkan tipe
    toastEl.classList.remove('bg-success', 'bg-danger');
    toastEl.classList.add(type === 'success' ? 'bg-success' : 'bg-danger');
    
    toastBody.innerText = message;
    
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
}

// 1. Fungsi Filter Universal (Mendukung pencarian teks dan rentang tanggal)
function filterData() {
    const start = document.getElementById("dateStart")?.value;
    const end = document.getElementById("dateEnd")?.value;
    const searchInput = document.getElementById("searchSO") || document.getElementById("searchGeneral");
    const searchText = searchInput ? searchInput.value.toUpperCase() : "";
    
    const rows = document.querySelectorAll("table tbody tr");

    rows.forEach(row => {
        const dateCell = row.querySelector(".cell-tanggal")?.innerText;
        const textCell = row.innerText.toUpperCase(); 
        
        let matchDate = true;
        if (dateCell && (start || end)) {
            const parts = dateCell.split('/');
            const rowDate = `${parts[2]}-${parts[1]}-${parts[0]}`;
            if (start && rowDate < start) matchDate = false;
            if (end && rowDate > end) matchDate = false;
        }

        let matchSearch = textCell.includes(searchText);

        if (matchDate && matchSearch) {
            row.style.display = "";
        } else {
            row.style.display = "none";
            const cb = row.querySelector('.row-check');
            if (cb) cb.checked = false;
        }
    });
}

// 2. Centang Semua (Hanya baris yang sedang tampil/filtered)
function toggleAll(source) {
    const rows = document.querySelectorAll("table tbody tr");
    rows.forEach(row => {
        if (row.style.display !== "none") {
            const cb = row.querySelector('.row-check');
            if (cb) cb.checked = source.checked;
        }
    });
}

// 3. Ekstraksi Data Universal (Untuk keperluan Excel & Email)
function getSelectedData() {
    let data = [];
    const headers = Array.from(document.querySelectorAll("table thead th"))
                         .map(th => th.innerText.trim())
                         .filter(h => h !== "" && h !== " " );

    document.querySelectorAll('.row-check:checked').forEach(cb => {
        let tr = cb.closest('tr');
        let rowData = {};
        let cells = Array.from(tr.querySelectorAll('td')).slice(1); 
        
        cells.forEach((cell, index) => {
            const key = headers[index] ? headers[index].replace(/\s+/g, '_').toUpperCase() : `COL_${index}`;
            rowData[key] = cell.innerText;
        });
        data.push(rowData);
    });
    return data;
}

// 4. Aksi Download Excel
function downloadSelected() {
    const data = getSelectedData();
    
    // Validasi menggunakan Toast
    if (data.length === 0) {
        return showToast("Gagal: Pilih data terlebih dahulu melalui checkbox!", "danger");
    }
    
    const input = document.getElementById('selectedRowsInput');
    const form = document.getElementById('downloadForm');
    
    if (input && form) {
        input.value = JSON.stringify(data);
        form.submit();
        showToast("Sukses: Laporan sedang diunduh ke perangkat Anda.");
    }
}

// 5. Aksi WhatsApp (Format Detail untuk Operasional)
function sendWhatsApp(dbName) {
    const selectedRows = document.querySelectorAll('table tbody tr:has(.row-check:checked)');
    
    if (selectedRows.length === 0) {
        return showToast("Gagal: Pilih baris data yang ingin dikirim ke WhatsApp!", "danger");
    }

    let message = `*Laporan Register SO - Database: ${dbName}*\n\n`;

    selectedRows.forEach((row, index) => {
        const noSO = row.querySelector('.cell-so-no')?.innerText || "-";
        const namaBarang = row.querySelector('.cell-nama')?.innerText || "-";
        const qty = row.querySelector('.cell-qty')?.innerText || "0";
        const packing = row.querySelector('.cell-packing')?.innerText || "-";

        message += `*${index + 1}. No SO:* ${noSO}\n`;
        message += `   *Barang:* ${namaBarang}\n`;
        message += `   *QTY:* ${qty}\n`;
        message += `   *Packing:* ${packing}\n`;
        message += `--------------------------\n`;
    });

    const note = prompt("Tambahkan catatan tambahan (opsional):");
    if (note) {
        message += `\n*Catatan:* ${note}`;
    }

    const whatsappUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

// 6. Aksi Email (Membuka Modal)
function openEmailModal() {
    if (getSelectedData().length === 0) {
        return showToast("Gagal: Pilih data yang ingin dikirim melalui email!", "danger");
    }
    emailBootstrapModal.show();
}

// 7. Proses Pengiriman Email via AJAX
async function processSendEmail() {
    const btn = document.getElementById('btnSendEmail');
    const email = document.getElementById('modalEmail').value;
    const note = document.getElementById('modalNote').value;
    const data = getSelectedData();

    if (!email) {
        return showToast("Peringatan: Alamat Email atau Group wajib diisi!", "danger");
    }

    // Indikator loading
    btn.innerText = "Sedang Mengirim...";
    btn.disabled = true;

    try {
        const response = await fetch(URL_SEND_EMAIL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                email: email,
                note: note,
                db: CURRENT_DB,
                data: data
            })
        });
        
        const res = await response.json();
        
        if (response.ok) {
            showToast(res.message, "success");
            emailBootstrapModal.hide();
            // Reset form modal
            document.getElementById('modalEmail').value = "";
            document.getElementById('modalNote').value = "";
        } else {
            showToast("Error: " + res.message, "danger");
        }
    } catch (e) {
        showToast("System Error: Gagal terhubung ke server mailer.", "danger");
    } finally {
        btn.innerText = "Kirim Sekarang";
        btn.disabled = false;
    }
}