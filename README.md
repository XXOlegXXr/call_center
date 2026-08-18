# Call Center Alert
An automated monitoring-to-notification system: when a critical infrastructure alert fires, the system automatically places a phone call to a real number via a SIP/VoIP trunk and sends an email, so a critical issue is never missed even if nobody is watching a dashboard.
```
Prometheus  →  Alertmanager  →  FastAPI  →  Asterisk PBX (Zadarma SIP trunk)  →  Phone call
                                    |
                                    |
                                    --------------------------------  Gmail (email alert) 
```

### The project turns a standard Linux monitoring stack (Prometheus + Alertmanager) into a system that can call a human on the phone. Alertmanager sends a webhook to a small FastAPI service, which triggers Asterisk to originate an outbound call through a Zadarma SIP trunk to a configured phone number, and in parallel sends an email notification via Gmail SMTP.

### It also includes a self-hosted Asterisk PBX with internal extensions, voicemail, call queues, and an escalation dialplan, originally built for a small call-center setup and repurposed here as the alerting/calling backend.


# /etc/prometheus/   :
```
/etc/prometheus/prometheus.yml
/etc/prometheus/disk-alert.yml
/etc/prometheus/alertmanager.yml

```

# SETUP


```
### 1. Asterisk
sudo systemctl restart asterisk
sudo asterisk -rx "pjsip show registrations"   # confirm Zadarma trunk: Registered

### 2. FastAPI service
cd api
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn python-dotenv
sudo systemctl enable --now call-center-api


#### 3. Prometheus / Alertmanager
sudo systemctl restart prometheus
sudo systemctl restart alertmanager


```






**Technologies Used**
- [x] VoIP/ATC: Asterisk 22.x
- [x] OS: Ubuntu Server
- [x] SIP trunk: Zadarma
- [x] Softphone: MicroSIP, Zoiper
- [x] Monitoring: Prometheus + node_exporter
- [x] Route alert: Alertmanager
- [x] Relay: FastAPI
- [x] Gmail message: Gmail SMTP
- [x] Server up: systemd
- [x] Config: pjsip.conf, extensions.conf, queues.conf, voicemail.conf


