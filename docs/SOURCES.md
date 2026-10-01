# Referensi resmi

Diperiksa 1 Oktober 2026 (WIB). Dokumentasi upstream berubah; digest/versi pilihan pengguna adalah sumber behavior deployment sebenarnya.

| Komponen | Referensi resmi | Digunakan untuk |
|---|---|---|
| Hermes Docker | https://hermes-agent.nousresearch.com/docs/user-guide/docker | `/opt/data`, `gateway run`, runtime ownership, persistence |
| Hermes providers | https://hermes-agent.nousresearch.com/docs/integrations/providers | `hermes model`, OpenAI Codex device flow, auth store, re-auth |
| Hermes configuration | https://hermes-agent.nousresearch.com/docs/user-guide/configuration | terminal backend, auxiliary title generation, precedence |
| Hermes CLI | https://hermes-agent.nousresearch.com/docs/reference/cli-commands/ | command reference |
| Hermes Telegram | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram | BotFather, token, allowed users, home chat |
| Hermes source | https://github.com/NousResearch/hermes-agent | toolset presets, upstream release/license |
| Docker Ubuntu | https://docs.docker.com/engine/install/ubuntu/ | Ubuntu 26.04 support, official APT repository, firewall limitation |
| Portainer CE Linux | https://docs.portainer.io/start/install-ce/server/docker/linux | image LTS, socket, HTTPS 9443, first-run setup token |
| Uptime Kuma | https://github.com/louislam/uptime-kuma | image major 2, data `/app/data`, localhost binding, no NFS |
| Tailscale Docker | https://tailscale.com/docs/features/containers/docker | container deployment |
| Tailscale parameters | https://tailscale.com/docs/features/containers/docker/docker-params | state directory and networking parameters |

Riwayat “Agentic AI Build” digunakan untuk error yang berhasil diambil: CLI restart-loop → `gateway run`; state `/opt/data`; OAuth inference berhasil; wrong model/provider; auxiliary title failure; config reload gateway; Telegram allowlist. Retrieval tidak memberikan seluruh transkrip sehingga daftar error tidak dinyatakan lengkap.
