---
name: ru-route
description: Reach Russian websites that refuse visitors from outside Russia, through the Russian VM whose login is in .env (SOCKS tunnel, browser identity, Playwright). Use when a Russian site times out, resets the connection or answers 403 from this machine.
---

This machine is outside Russia. Many Russian sites, official ones especially, refuse foreign connections, so a timeout, reset or 403 may mean geo-blocking, not a dead site. Route such requests through the Russian VM whose login is in .env (SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASS).

Credentials

- Never print, log or write the values, and keep the VM's address out of every file you write.
- Load them only inside the command that uses them (`set -a; . ./.env; set +a`), and pass the password as `SSHPASS="$SFTP_PASS" sshpass -e ssh …`, never on the command line.

Route

1. Open a SOCKS tunnel in the background: `ssh -p "$SFTP_PORT" -o StrictHostKeyChecking=accept-new -o PreferredAuthentications=password,keyboard-interactive -o PubkeyAuthentication=no -f -N -M -S <socket> -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 -D 127.0.0.1:1080 "$SFTP_USER@$SFTP_HOST"` (through sshpass as above). Keep the control socket path short, under /tmp: Unix socket paths are limited to about 100 characters.
2. Confirm the exit is in Russia: `curl -s --socks5-hostname 127.0.0.1:1080 https://ipinfo.io/country` prints RU.
3. Fetch documents and plain pages with curl through the tunnel (`--socks5-hostname 127.0.0.1:1080`), always with a normal browser User-Agent and `Accept-Language: ru-RU`: with curl's default identity, official sites answer 403 or drop the connection silently.
4. For pages built by JavaScript, or when curl gets a challenge page, use Playwright: `uv run --with playwright`, the system Chrome (channel "chrome"), proxy `socks5://127.0.0.1:1080`, locale ru-RU, and a fresh page for each URL (in a reused tab, one failed load corrupts the next).
5. If https:// times out, try http://. A site counts as unreachable only after both schemes and the browser have failed through the tunnel; record that with the date rather than calling the site dead.
6. If the tunnel can't be opened but a shell works, run curl on the VM over ssh instead. Install nothing on the VM.
7. Close the tunnel when done (`ssh -S <socket> -O exit "$SFTP_USER@$SFTP_HOST"`) and check that no ssh process is left.

Limits

- Use the route only for Russian sites that fail directly; foreign sites may be slowed or blocked from Russia.

Observed on 2026-10-28: rkn.gov.ru answered 403 to curl's default identity and 200 to a browser User-Agent; government.ru did not answer on https even from inside Russia, but answered on http.
