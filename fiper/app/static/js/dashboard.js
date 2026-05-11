/**
 * FIPER Dashboard Logic
 * Real-time log streaming menggunakan polling 2 detik
 */

function fetchLogs() {
    // Menggunakan rute dinamis dari window.LOG_API_URL yang diset di index.html
    const targetUrl = window.LOG_API_URL || '/get_logs';

    fetch(targetUrl)
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            const logBox = document.getElementById('log-box');
            if (!logBox) return;

            if (data.length > 0) {
                logBox.innerHTML = data.map(log => `
                    <div class="mb-1" style="border-bottom: 1px solid #333; padding-bottom: 2px;">
                        <span class="text-secondary small">[${log.time}]</span> 
                        <span style="color: #00d4ff">IP: ${log.ip}</span> - 
                        <span class="text-light">${log.action}</span> 
                        <span style="color: #ffcc00">(${log.db})</span> - 
                        <span class="text-success fw-bold">SUCCESS</span>
                    </div>
                `).join('');
                
                // Opsional: hapus scrollTop jika ingin data terbaru tetap di atas tanpa scroll otomatis
                // logBox.scrollTop = 0; 
            } else {
                logBox.innerHTML = '<div class="text-muted text-center mt-3 small">[ Belum ada aktivitas tercatat ]</div>';
            }
        })
        .catch(err => console.error("Log fetch error:", err));
}

function navigate(basePath) {
    const dbSelect = document.getElementById('db_select');
    if (!dbSelect) return;
    
    const selectedDb = dbSelect.value;
    window.location.href = `${basePath}?db=${selectedDb}`;
}

// Jalankan polling setiap 2 detik setelah DOM siap
document.addEventListener('DOMContentLoaded', () => {
    fetchLogs(); // Ambil segera saat load
    setInterval(fetchLogs, 2000);
});