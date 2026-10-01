# Publikasikan ke GitHub

Repository utama: https://github.com/thuekx/hermes-docker-starter. Panduan berikut untuk pengguna yang ingin membuat fork atau menerbitkan salinan sendiri.

1. Ekstrak paket lalu review file. Buat repository kosong di GitHub, pilih nama sendiri dan visibility sesuai tujuan berbagi.
2. Jangan jalankan `git add .` setelah instalasi tanpa mengecek ignored files.
3. Dari folder project:

```bash
git init -b main
git add README.md LICENSE NOTICE.md SECURITY.md CONTRIBUTING.md CHANGELOG.md install.sh scripts docs tests .github .gitignore
git diff --cached --stat
git diff --cached --check
read -r -p 'Git author name Anda: ' GIT_AUTHOR_NAME
read -r -p 'Git email/noreply address Anda: ' GIT_AUTHOR_EMAIL
git -c user.name="$GIT_AUTHOR_NAME" -c user.email="$GIT_AUTHOR_EMAIL" commit -m 'Initial single-bot Hermes Docker installer'
read -r -p 'URL repository GitHub tujuan (SSH/HTTPS): ' GITHUB_REPO_URL
git remote add origin "$GITHUB_REPO_URL"
git push -u origin main
```

Atribusi program **thuekx** tetap di README/NOTICE; identitas Git committer harus sesuai pengguna yang melakukan upload. Autentikasi GitHub lewat SSH key/credential manager pribadi; jangan menaruh PAT dalam URL atau file.

4. Aktifkan Actions dan private vulnerability reporting pada repository jika tersedia. CI memvalidasi code/Compose, bukan login OAuth/Telegram.
5. Pengguna lain memakai `git clone` pada instalasi pertama, kemudian `git pull --ff-only` untuk update source. OAuth, token, nama, username dan password tetap diisi sendiri.

Sebelum push, pastikan `git status --ignored` menunjukkan `.runtime/`/secrets sebagai ignored. Data runtime berada di luar clone dan tidak ikut commit. Jangan upload backup ZIP yang Anda buat dari folder runtime.
