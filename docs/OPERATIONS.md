# Operations — backup, restore, upgrade

## Backup konsisten

```bash
python3 scripts/manage.py backup
```

Backup menghentikan semua service, mengarsip Hermes/workspace/Portainer/Kuma/Tailscale dan settings/Compose, lalu menyalakan kembali **hanya service yang sebelumnya berjalan**, termasuk bila tar gagal. Ada downtime. Archive mode 0600 di `<DATA_DIR>/backups`; mengandung OAuth, bot token, history, dan VPN state. Pindahkan salinan terenkripsi ke tempat aman. Snapshot VMware hidup tidak menggantikan backup aplikasi yang konsisten.

## Restore offline ke server yang sama

1. Stop stack: `python3 scripts/manage.py stop`.
2. Pilih backup dan direktori staging **baru**; ekstrak archive yang Anda percaya di staging. Jangan mengekstrak langsung ke `/` atau direktori data aktif.
3. Pastikan archive berisi `hermes/`, `workspace/`, `portainer/`, `kuma/`, `tailscale/`, `settings.json`, `compose.json`.
4. Simpan data saat ini sebagai salinan rollback. Gantikan kelima direktori data dengan salinan dari staging menggunakan sudo agar ownership terjaga.
5. Pulihkan `settings.json` dan `compose.json` ke `.runtime/` hanya bila path/project/server sama; mode 0600. Direktori `.runtime` mode 0700.
6. `python3 scripts/manage.py validate`, lalu `start`.
7. Tes OAuth, Telegram, file workspace, panel, dan Tailscale.

Restore ke server lain: ubah path bind source pada Compose dan `data_dir`/SSH settings agar sesuai server baru. **Server lama harus offline** sebelum state bot/Tailscale yang sama dinyalakan di server baru. Jangan menjalankan dua gateway atau dua node dengan state yang sama. Re-auth Tailscale lebih disarankan ketika migrasi identitas host; jangan mengunggah auth state ke issue.

## Upgrade source installer

```bash
git pull --ff-only
python3 -m unittest discover -s tests -v
python3 scripts/manage.py validate
```

Pull source **tidak mengubah image pinned**. Baca release notes dan perubahan schema sebelum melanjutkan. File `.runtime` serta data di luar repository dipertahankan.

## Upgrade image terkontrol

1. `backup` sebelum perubahan. Catat digest lama di settings/Compose privat.
2. Uji versi kandidat pada VM/container dengan state baru dan bot berbeda. Jangan reuse bot/state aktif untuk uji.
3. Edit referensi image service yang ingin diperbarui di `.runtime/compose.json` dan key image terkait di `.runtime/settings.json`; masukkan digest kandidat yang telah diverifikasi dari registry resmi.
4. `validate` lalu pull dan recreate **service yang dipilih**:

```bash
read -r -p 'Service yang diuji (hermes/portainer/kuma/tailscale): ' SERVICE
case "$SERVICE" in hermes|portainer|kuma|tailscale) ;; *) exit 1 ;; esac
sudo docker compose -f .runtime/compose.json pull "$SERVICE"
sudo docker compose -f .runtime/compose.json up -d --force-recreate "$SERVICE"
```

5. Jalankan acceptance. Bila schema data sudah bermigrasi, mengganti image ke versi lama saja belum tentu cukup: restore backup offline **dan digest lama**.

Jangan `hermes update` di dalam image official untuk mengganti core installed tree; upgrade image. Jangan pasang Watchtower/auto-update untuk stack OAuth ini tanpa regression test dan backup.

## Uninstall

`stop` menjaga seluruh data. Untuk melepas container/network, `sudo docker compose -f .runtime/compose.json down` tanpa `-v`. Penghapusan data dilakukan manual hanya setelah backup berhasil diverifikasi. Tidak ada perintah wipe otomatis.
