# Contributors welcome

Terima kasih telah membantu membuat installer ini lebih mudah direproduksi. Author/maintainer awal: **thuekx**.

## Fokus kontribusi

- Acceptance pada Ubuntu 26.04 amd64/arm64 dengan image digest yang dicatat.
- Compatibility test entrypoint Hermes, OAuth, model, Telegram, dan upgrade/restore.
- Dokumentasi Bahasa Indonesia/English, accessibility, dan onboarding yang jelas.
- Monitoring kesehatan inference authenticated tanpa memberikan host Docker socket ke agent.

## Alur PR

1. Fork repository dan buat branch dari main.
2. Jelaskan masalah, behavior sebelum/sesudah, batasan, dan bukti tes.
3. Jalankan:

```bash
bash -n install.sh scripts/install-docker.sh
python3 -m unittest discover -s tests -v
```

4. Untuk Compose, jalankan workflow CI/validasi pada host Docker. Untuk perubahan lifecycle, uji di VM khusus, gunakan bot/account sendiri dan data baru.
5. Tidak boleh menyertakan `.runtime`, tokens, auth.json, `.env`, chat history, screenshots login, logs mentah, IP/hostname privat atau backup.
6. Buat PR dengan checklist template. Tandai apakah tes real atau mock; jangan klaim OAuth/Telegram lulus tanpa tes nyata.

Kode baru original menggunakan SPDX `GPL-3.0-or-later`. Dengan mengirim kontribusi Anda setuju kontribusi original dilisensikan GPL-3.0-or-later. Lisensi upstream dependency harus dipertahankan. Jangan menambahkan CLA atau persyaratan kontribusi yang tidak disepakati maintainer.
