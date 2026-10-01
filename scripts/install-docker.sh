#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Jalankan: sudo bash scripts/install-docker.sh'; exit 1; }
source /etc/os-release
[[ ${ID:-} == ubuntu && ${VERSION_ID:-} == 26.04 ]] || {
  echo 'Bootstrap ini ditargetkan khusus Ubuntu 26.04. OS lain: instal Docker mengikuti dokumentasi resmi.'; exit 1;
}
if command -v docker >/dev/null; then
  docker info >/dev/null
  docker compose version
  echo 'Docker yang ada dipertahankan; tidak di-upgrade oleh bootstrap.'
  exit 0
fi
for pkg in docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc; do
  if dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q 'install ok installed'; then
    echo "Paket konflik ditemukan: $pkg. Tinjau workload dan hapus konflik secara manual; installer berhenti."
    exit 1
  fi
done
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl python3 git tzdata
install -m 0755 -d /etc/apt/keyrings
curl --proto '=https' --tlsv1.2 -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
arch=$(dpkg --print-architecture)
cat > /etc/apt/sources.list.d/docker.sources <<REPO
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: ${UBUNTU_CODENAME:-$VERSION_CODENAME}
Components: stable
Architectures: $arch
Signed-By: /etc/apt/keyrings/docker.asc
REPO
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable --now docker
docker run --rm hello-world
docker compose version
echo 'Docker siap. User tidak otomatis dimasukkan ke grup docker (akses setara root).'
