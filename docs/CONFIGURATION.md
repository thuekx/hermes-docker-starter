# Configuration — semua identitas milik pengguna

| Isian | Contoh saja | Tempat input |
|---|---|---|
| Username / password Ubuntu / SSH key | `john` / password pribadi | Installer Ubuntu dan administrasi OS |
| Compose project | `john-ai` | Wizard; menjadi prefix container/network otomatis |
| Owner / assistant | `John Doe` / `John AI` | Wizard, kemudian SOUL.md |
| IP/hostname dan port SSH | `192.0.2.10` / `22` | Wizard; hanya untuk mencetak tunnel |
| Timezone | `Asia/Jakarta` | Wizard |
| Direktori data absolute dan baru | `/home/john/services/john-ai` | Wizard |
| Tag/digest setiap image | Contoh di README | Wizard; dipin ke digest setelah pull |
| Nama node Tailscale | `john-ai-node` | Wizard |
| Port panel lokal | `9443` / `3001` | Wizard; boleh diubah dan harus berbeda |
| Display name / username bot | `John AI` / nama unik berakhiran `bot` | @BotFather |
| Telegram bot token | Token dari BotFather | Wizard dengan input tersembunyi |
| Telegram user ID allowlist | `123456789` | Wizard; user manusia, bukan bot/chat group |
| Provider dan model | OpenAI Codex / model dari daftar akun | Wizard upstream `hermes model` |
| Email/password/MFA OpenAI | Akun pribadi | Hanya browser login resmi |
| Portainer admin username/password | Isi sendiri | First-run UI Portainer |
| Kuma admin username/password dan monitor names | Isi sendiri | First-run UI Kuma |
| Tailscale akun/tailnet | Pilih sendiri | Browser resmi saat `tailscale up` |
| API key tool tambahan | Sesuai provider pilihan | Opsional `hermes tools`; di luar instalasi inti |

Nilai infrastruktur seperti `/opt/data`, `/workspace`, service keys `hermes`, `portainer`, `kuma`, dan `tailscale` adalah interface internal software, bukan identitas user. Author `thuekx` adalah atribusi lisensi yang memang diminta, bukan nama asisten/default user.

Wizard tidak menyimpan token Telegram di settings Compose. Token ada di `<DATA_DIR>/hermes/.env` dengan mode 0600; OAuth dikelola Hermes di data persisten. Metadata nonsecret tersimpan di `.runtime/settings.json`; file Compose generated di `.runtime/compose.json` adalah JSON valid untuk Docker Compose. Keduanya diabaikan Git. Jangan menampilkan `.env` atau auth.json ke publik.

## Telegram ID tanpa bot pihak ketiga

Sebelum gateway dimulai, kirim `/start` ke bot Anda lalu jalankan skrip berikut dari terminal privat. Token diminta tersembunyi dan tidak muncul di command line:

```bash
python3 - <<'PY'
import getpass, json, urllib.request
secret = getpass.getpass('Bot token: ')
try:
    with urllib.request.urlopen('https://api.telegram.org/bot'+secret+'/getUpdates', timeout=20) as response:
        data = json.load(response)
    for update in data.get('result', []):
        sender = update.get('message', {}).get('from', {})
        if sender and not sender.get('is_bot'):
            print('USER ID:', sender['id'])
except Exception:
    print('Tidak dapat mengambil update. Periksa token, koneksi, dan apakah gateway lain memakai bot ini.')
PY
```

Jangan jalankan `getUpdates` ini ketika gateway aktif, karena akan berebut polling. Empty result: kirim pesan baru ke bot. Existing webhook: jangan hapus tanpa memeriksa sistem yang menggunakannya; paling disarankan bot baru.

## Ubah konfigurasi setelah instalasi

Nama asisten/pemilik: edit `<DATA_DIR>/hermes/SOUL.md` dengan izin yang benar, kemudian restart Hermes. Model/provider: `python3 scripts/manage.py login`. Token/user allowlist: `rotate-telegram` (menjaga API key tambahan). Monitor names/admin account: ubah di UI. SSH target yang dicetak: edit `.runtime/settings.json` secara lokal; perintah `access` membacanya.

Untuk mengganti project/path/node/image, ikuti operasi backup dan upgrade; jangan mengubah path state ke direktori lain tanpa migrasi data. File Hermes yang dimiliki runtime user bisa diedit via `sudoedit`; jangan `chmod 777`.
