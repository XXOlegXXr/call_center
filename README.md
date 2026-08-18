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
~~ VoIP/ATC: Asterisk 22.x ~~
~~OS: Ubuntu Server ~~
~~ Sip trank: Zadarma ~~
~~Softphone: MicroSIP, Zoiper ~~
~~ Monitoring: Prometheus + node_exporter ~~
~~ Route alert: alertmanager ~~
~~Ralay: FastAPI ~~
~~ Gmail message: POSTFIX, Gmail SMTP ~~
~~ server up: systemd ~~
~~ Config: pjsip.conf, extensions.conf, queues.conf, voicemail.conf ~~



