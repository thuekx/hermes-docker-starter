# Validation & acceptance

## Hasil pembuatan paket — 2026-10-01 WIB

| Pemeriksaan | Status | Batas bukti |
|---|---|---|
| Syntax Bash | PASS | `bash -n` pada entrypoint dan bootstrap |
| Python compilation | PASS | Python 3 di lingkungan pembuatan |
| Unit tests | PASS | 14 pengujian offline; termasuk lifecycle sukses/gagal, backup failure recovery dan secret separation |
| Compose structure, lifecycle, secret separation | PASS offline | Fixture/mock, bukan container hidup |
| Docker Compose `config --quiet` | PASS di CI | Berjalan pada GitHub Actions Ubuntu 24.04; Docker tidak tersedia di lingkungan pembuatan lokal |
| GitHub Actions | PASS | [Run #1](https://github.com/thuekx/hermes-docker-starter/actions/runs/36871925625): Bash syntax, 14 tes Python, Docker Compose config |
| Install Ubuntu 26.04 | BELUM DIUJI DI SINI | OS target, bukan klaim hasil tes mesin pengguna |
| OpenAI OAuth inference | PERLU ACCEPTANCE USER | Tidak memakai akun/token milik author |
| Telegram send/receive/tools | PERLU ACCEPTANCE USER | Tidak memakai bot milik author |
| Portainer/Kuma/Tailscale runtime | PERLU ACCEPTANCE USER | Akun UI/login tailnet diisi sendiri |

Riwayat sumber berisi setup Hermes yang sudah sukses; itu tidak sama dengan pengujian paket installer baru. Pemeriksaan dokumentasi resmi Docker mengonfirmasi Ubuntu 26.04 sebagai OS yang didukung, tetapi tidak menjamin seluruh stack ini sudah lulus acceptance.

## Jalankan tes offline

```bash
bash -n install.sh scripts/install-docker.sh
python3 -m py_compile scripts/manage.py
python3 -m unittest discover -s tests -v
```

Pada host Docker setelah wizard: `python3 scripts/manage.py validate`. Workflow Actions memakai Ubuntu 24.04 runner untuk tes script/Compose; **tidak** mengklaim tes instalasi Ubuntu 26.04.

## Acceptance pada VM Ubuntu 26.04 baru

Catat OS, architecture, Docker/Compose version, dan digest setiap image tanpa token.

- [ ] Docker hello-world berjalan dan Compose plugin tersedia.
- [ ] Semua nama/identitas/path diisi sendiri; state berada di disk lokal di luar Git clone.
- [ ] Semua image berhasil dipull dan dikunci digest, Compose valid.
- [ ] Wizard benar-benar memilih provider `openai-codex` dan model yang tersedia.
- [ ] Browser device flow selesai dan model membalas `HERMES OPENAI OAUTH OK`.
- [ ] Akun Portainer/Kuma dibuat sendiri, password unik; admin panels hanya loopback.
- [ ] Tailscale node visible dalam tailnet dan SSH tunnel via Tailscale bekerja.
- [ ] Bot Telegram membalas DM user allowlist, tanpa menu pemilihan persona/orang.
- [ ] Akun kedua yang TIDAK dalam allowlist ditolak/tidak mendapat akses agent.
- [ ] Tool membuat dan membaca `/workspace/hello.txt` tanpa akses host filesystem.
- [ ] Restart Hermes; config, OAuth dan file workspace tetap ada; bot masih membalas.
- [ ] Tidak ada host gateway/poller kedua memakai bot yang sama.
- [ ] Monitor Kuma sesuai target; notifikasi sendMessage pada bot yang sama berhasil bila diaktifkan.
- [ ] Backup konsisten berhasil dan restore diuji offline ke staging/VM uji.
- [ ] Reboot Ubuntu; Docker services restart dan Tailscale reconnect.
- [ ] Git tracked files tidak berisi secret atau runtime state.

Installer merekam acceptance.json berdasarkan jawaban pengguna setelah inference dan Telegram: itu konfirmasi manusia, bukan pengganti bukti semua checklist di atas.
