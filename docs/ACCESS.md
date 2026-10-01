# Akses privat — localhost, SSH, Tailscale

1. Jalankan `python3 scripts/manage.py access` di server.
2. Salin command tunnel yang dicetak ke terminal laptop. User, SSH host, dan port berasal dari input Anda.
3. Buka URL localhost Portainer/Kuma yang dicetak.
4. Setelah Tailscale login, ganti **host SSH** pada command tunnel menjadi IP node Tailscale; local-forward tujuan tetap `127.0.0.1`.
5. SSH di host harus berjalan dan listening pada interface yang menerima Tailscale. Tailscale container bukan server SSH: tunnel memakai OpenSSH Ubuntu host.

Portainer menggunakan HTTPS self-signed bawaan. Verifikasi server/tunnel yang dituju; pada lingkungan sendiri sertifikat perlu dipercaya atau exception browser lokal. Pasang sertifikat yang valid untuk penggunaan lebih luas. Kuma HTTP hanya melalui tunnel yang terenkripsi. Tidak ada port API/dashboard Hermes yang dipublish; Telegram memakai outbound polling dan tidak butuh inbound webhook port.

> [!WARNING]
> Published Docker ports dapat melewati aturan UFW. Gunakan binding localhost seperti template; jangan mempublish Docker API TCP 2375/2376 atau admin panel ke internet. Tailscale tidak menggantikan login admin aplikasi, SSH key, atau pembatasan user bot.

## Browser PKCE bila device OAuth dilarang organisasi

Default installer memakai device flow. Pilihan browser PKCE membutuhkan port callback 1455 tetap dari upstream. Siapkan tunnel laptop → host 1455 dan publish **loopback-only** port 1455 → container one-shot 1455. Wizard biasa tidak mempublish callback itu. Ini alur lanjutan, bukan alasan mempublish port ke internet. Ikuti dokumentasi resmi OAuth over SSH di SOURCES.md dan jalankan `hermes auth add openai-codex --browser` dalam container login yang mempunyai mapping callback tersebut; jangan mengubah port callback terdaftar.
