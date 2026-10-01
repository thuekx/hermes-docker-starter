# Uptime Kuma — monitor yang tidak menyesatkan

Kuma dipasang otomatis; akun, nama monitor, interval, dan password diisi manual lewat UI. Paket tidak mengandalkan API setup Kuma internal.

## Monitor dasar

Di UI → Add New Monitor:

| Jenis | Nama (input Anda) | Target | Makna |
|---|---|---|---|
| HTTP(s) | Contoh `John Portainer` | `https://portainer:9443` | Panel admin merespons dari network management |
| HTTP(s) | Contoh `John Kuma Self` | `http://127.0.0.1:3001` | Proses Kuma merespons dari container sendiri |

Untuk self-signed Portainer, gunakan opsi Ignore TLS/SSL error **hanya monitor lokal ini**. Ini tidak mengubah validasi TLS OAuth. Interval contoh 60 detik, retries 3 — diisi sendiri sesuai kebutuhan. `localhost` di dalam Kuma adalah container Kuma, bukan Ubuntu host atau container Hermes.

## Hermes dan Telegram

Tidak disediakan HTTP health endpoint palsu yang hanya membuktikan container hidup. Stack inti tidak membuka API Hermes. Kombinasikan:

1. `status` dan `logs hermes` untuk proses/restart error.
2. `doctor` untuk konfigurasi/provider.
3. Pesan DM ke bot sebagai tes jalur Telegram → model → balasan.
4. Tes OAuth inference saat onboarding dan setelah update.

Kuma mendeteksi ketersediaan panel, **bukan kemampuan inference OAuth atau polling Telegram**. Tidak memberi Docker socket kepada Kuma/Hermes merupakan pilihan isolasi. Health check aplikasi lengkap bisa ditambahkan lewat kontribusi terpisah, dengan endpoint authenticated dan verifikasi model, tanpa mengklaim container `running` sebagai bot sehat.

## Notifikasi memakai satu bot yang sama

Kuma → Settings → Notifications → Telegram: isi token **bot yang sama** dan chat ID pribadi sendiri, lalu Test. Kuma mengirim pesan lewat `sendMessage`; jangan menjalankan receiver/getUpdates lain. Ini tetap satu bot. Token kini juga tersimpan di state Kuma: perlakukan backup Kuma sebagai rahasia. Telegram `/sethome` mengatur tujuan Hermes; tidak otomatis mengisi chat ID di Kuma.
