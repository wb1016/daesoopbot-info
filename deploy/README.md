# Deployment guide — daesoop.sudden.ninja

Target layout on the VM (Oracle Cloud, Korea region):

```
/opt/daesoop/
├── bamboozleify-bot/    # code repo (Discord bot)
│   ├── .env             # BAMBOOZLEIFY_TOKEN=...
│   └── .venv/
└── daesoopbot-info/     # this repo (info pages + web server)
    └── .venv/
```

## 1. VM preparation

```bash
sudo adduser --disabled-password --gecos "" daesoop
sudo mkdir -p /opt/daesoop && sudo chown daesoop:daesoop /opt/daesoop
sudo apt update && sudo apt install -y nginx certbot python3-certbot-nginx

# as daesoop (or root, then chown):
cd /opt/daesoop
git clone <code-repo-url> bamboozleify-bot
git clone <info-repo-url> daesoopbot-info

cd /opt/daesoop/bamboozleify-bot
uv venv -p 3.14 && uv pip install -e .
cp .env.example .env   # put BAMBOOZLEIFY_TOKEN in it

cd /opt/daesoop/daesoopbot-info
uv venv -p 3.14 && uv pip install -e .
```

## 2. DNS

Add an A record: `daesoop.sudden.ninja` → the VM's public IP.

## 3. Open ports 80/443 (Oracle-specific!)

Oracle Cloud blocks traffic in **two** places — both must be opened:

1. **OCI console** → instance → VNIC → Security List (or NSG): add ingress rules
   for TCP 80 and TCP 443 from `0.0.0.0/0`.
2. **The VM itself** (Ubuntu images ship with restrictive iptables):

```bash
sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save   # or iptables-persistent equivalent
```

## 4. systemd services

```bash
sudo cp /opt/daesoop/daesoopbot-info/deploy/daesoop-web.service /etc/systemd/system/
sudo cp /opt/daesoop/daesoopbot-info/deploy/bamboozleify-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now daesoop-web.service bamboozleify-bot.service
systemctl status daesoop-web bamboozleify-bot
curl http://127.0.0.1:8000/health   # → ok
```

## 5. nginx + TLS (certbot)

```bash
sudo cp /opt/daesoop/daesoopbot-info/deploy/nginx-daesoop.conf /etc/nginx/sites-available/daesoop
sudo ln -s /etc/nginx/sites-available/daesoop /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

sudo certbot --nginx -d daesoop.sudden.ninja
```

certbot edits the site file to add the 443 block + HTTP→HTTPS redirect and
installs a renewal timer (`systemctl list-timers | grep certbot` to confirm).
Renewal uses the nginx plugin, so no downtime.

Verify: `curl -I https://daesoop.sudden.ninja/terms` → 200.

## 6. Discord Developer Portal

App settings → paste:

- Terms of Service URL: `https://daesoop.sudden.ninja/terms`
- Privacy Policy URL: `https://daesoop.sudden.ninja/privacy`

(Korean/English is negotiated from the visitor's `Accept-Language`; explicit
URLs like `/terms/ko` and `/terms/en` also exist.)

## 7. Updating content

Info pages: `git -C /opt/daesoop/daesoopbot-info pull` — no restart needed
(pages are re-rendered when the file mtime changes). Bot code: pull, then
`uv pip install -e .` if deps changed, and `sudo systemctl restart bamboozleify-bot`.
