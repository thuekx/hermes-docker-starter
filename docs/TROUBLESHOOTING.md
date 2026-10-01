# Troubleshooting — symptom → fix

| Symptom | Penyebab / langkah pemeriksaan | Perbaikan |
|---|---|---|
| Container Hermes restart loop saat awal | CLI interaktif dipakai sebagai daemon | Compose memakai `command: [gateway, run]`, bukan CLI tanpa command |
| Config/OAuth hilang setelah recreate | Data volume salah | Pertahankan satu mount `<DATA_DIR>/hermes` → `/opt/data`; jangan `down -v`/hapus data |
| Claude gagal melalui Codex | Provider/model tidak cocok | `login` → OpenAI Codex → model yang tersedia pada akun, kemudian `start` |
| Inference sukses tetapi error title generation | Auxiliary provider mempunyai auth/model berbeda | Installer menonaktifkan title generation; provider auxiliary auto dan model kosong |
| `gateway already running` / Telegram 409 Conflict | Ada host gateway atau bot poller lain | Hentikan **gateway yang Anda verifikasi memakai token ini**; jangan jalankan dua gateway; bot baru paling disarankan |
| Telegram diam setelah token/config berubah | Proses lama belum reload | `rotate-telegram` atau `restart hermes`, lalu kirim `/start` dan tes DM |
| Unauthorized | User ID salah/tidak ada di allowlist | Masukkan ID akun manusia, bukan username/ID bot/chat group; jangan enable allow-all |
| Pairing di Docker tidak terbaca | File pairing dibuat root | Gunakan `docker compose -f .runtime/compose.json exec -u hermes hermes hermes pairing …`; jangan root |
| `Permission denied` workspace/state | UID image berbeda atau file dibuat root | Installer membaca UID/GID `hermes` dari image dan hanya chown workspace; state diatur entrypoint resmi. Jangan chmod 777 |
| Docker socket permission denied | User tidak mempunyai akses Docker | Script memakai sudo; jangan mount socket ke Hermes untuk mengatasinya |
| Image/tag tidak ditemukan | Salah input/tag upstream berubah | Verifikasi registry resmi, ubah referensi settings setelah backup; tidak mengganti ke dev image secara diam-diam |
| Portainer first-run timeout / setup token diminta | Setup UI belum dilakukan atau versi memakai setup token | Restart Portainer, buka segera melalui tunnel; baca logs privat untuk setup token |
| Kuma/Portainer tidak dapat dibuka via IP Tailscale | Panel bind localhost | Gunakan SSH tunnel via IP Tailscale sesuai ACCESS.md |
| Tailscale `/dev/net/tun` hilang | VM/VPS belum menyediakan TUN | Aktifkan TUN di hypervisor/VPS; jangan `privileged: true` sebagai tebakan |
| Tailscale login belum terhubung | Browser approval/key expiry/ACL | `tailscale-login`, verifikasi admin console serta grants; jangan membagikan tailnet terbuka |
| OAuth expired/invalid_grant | Credential dicabut/refresh gagal | `login`, autentikasi ulang akun sendiri, lalu `start`; jangan menyalin token author |
| OAuth SSL EOF atau timeout | DNS, jam sistem, outbound firewall, TLS proxy/middlebox | Periksa NTP/DNS/proxy, lihat dokumentasi upstream TLS. Jangan disable TLS verification |
| Script terhenti | Ada step/user acceptance gagal | Konfigurasi dipertahankan; perbaiki step lalu ulangi. UI/daemon yang sudah dimulai tetap berjalan |
| Snapshot/backup merusak session | Writer SQLite masih berjalan saat salin | Gunakan backup offline yang menghentikan stack lalu memulai layanan yang sebelumnya berjalan |

## Menemukan gateway host lama tanpa mematikannya sembarang

```bash
systemctl --user status hermes-gateway.service
systemctl status hermes-gateway.service
```

Periksa mesin asal dan service yang memang Anda miliki. Hentikan service terkait hanya setelah memastikan service itu bukan bot/workload lain. Installer tidak membunuh service host otomatis karena tidak mengetahui kepemilikannya. Jangan jalankan `hermes gateway start` atau systemd host tambahan untuk deployment Compose ini.

Log dapat berisi chat, device code, token, dan setup token. Hapus informasi rahasia sebelum mengirim bug report. Ringkasan ini berdasarkan error yang berhasil ditelusuri pada percakapan asal; tidak mengklaim seluruh transkrip telah diperiksa.
