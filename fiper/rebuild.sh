#!/bin/bash
echo "--- Memulai proses rebuild kontainer ---"
docker build -t fina-piutang-app .
docker rm -f fina-container
docker run -d --name fina-container --network net-caddy -p 5000:5000 -e TZ=Asia/Jakarta -v $(pwd)/activity_logs.json:/app/activity_logs.json fina-piutang-app
echo "--- Selesai! Kontainer sudah berjalan kembali ---"
echo "--- logs report ---"
docker logs -f fina-container
