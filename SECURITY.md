# Security

Kode installer original © 2026 thuekx. GPL-3.0-or-later tidak memberikan garansi.

## Batas akses

- Allowed Telegram users saja; allow-all false. Bot mempunyai terminal/file tools di container dan dapat membaca state yang memang tersedia di sana.
- Docker container bukan isolasi setara VM. Untuk pekerjaan agent pada infrastruktur nyata, pakai VM khusus dan credential dengan hak minimum.
- Hermes tidak mendapat Docker socket, host filesystem root, privileged mode, host network, SSH key host, atau vCenter credential.
- Portainer mendapat Docker socket dan karena itu mempunyai kuasa administratif host Docker. Lindungi akun admin dan tunnel. Mount socket read-only bukan jaminan API Docker read-only.
- Tailscale memakai NET_ADMIN/NET_RAW dan host network untuk VPN, dengan state privat. Ini akses khusus komponen VPN, tidak diberikan ke Hermes.
- Panel bind 127.0.0.1; SSH key, tailnet ACL/grant, admin login dan 2FA bila tersedia tetap diperlukan.
- SOUL.md instruksi bukan security boundary; output web/chat/file dapat berisi prompt injection. Agent bisa membaca token OAuth/bot dalam state yang diperlukan runtime. Jangan memasukkan credential tambahan berhak luas.

## Do

Gunakan bot baru, user ID allowlist, disk lokal, digest pin, password unik, SSH key, backup offline terenkripsi, dan review source sebelum sudo. Simpan runtime di luar repository. Verifikasi DNS/NTP/TLS server. Tinjau task destructive sebelum menyetujui.

## Don't

Jangan allow-all, publish 2375/2376, mount Docker socket ke Hermes/Kuma, mount host root, disable TLS verification, gunakan chmod 777, `down -v`, reuse bot aktif di deployment kedua, atau commit state/log/config privat. Jangan memasukkan username/password OpenAI ke issue atau installer.

## Secret bocor

1. Revoke token bot di BotFather lalu `rotate-telegram`.
2. Cabut/re-auth sesi OAuth dari akun terkait sesuai kontrol provider.
3. Revoke node/key Tailscale jika state VPN bocor.
4. Rotasi admin passwords dan tool API keys terkait.
5. Hapus secret dari Git history bila sudah terlanjur commit; menghapus file pada commit baru tidak menghapus sejarah.

Laporkan kerentanan melalui **GitHub private vulnerability reporting** pada repository jika maintainer telah mengaktifkannya. Jangan posting detail exploit/credential di public issue. Jika belum tersedia, minta maintainer menyiapkan kanal privat tanpa menyertakan detail sensitif. Tidak ada alamat email maintainer yang dibuat-buat.
