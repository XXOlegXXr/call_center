1. Asterisk — Fix Conflicting Voicemail Modules

Two voicemail storage backends (app_voicemail_imap.so, app_voicemail_odbc.so) conflict with the default app_voicemail.so and prevent clean module load.

# 1. Move conflicting modules out of the load path
sudo mkdir -p /root/asterisk-modules-disabled
sudo mv /usr/lib/x86_64-linux-gnu/asterisk/modules/app_voicemail_imap.so /root/asterisk-modules-disabled/
sudo mv /usr/lib/x86_64-linux-gnu/asterisk/modules/app_voicemail_odbc.so /root/asterisk-modules-disabled/

# 2. Full restart and wait for init
sudo systemctl restart asterisk
sleep 3

# 3. Verify
sudo asterisk -rx "core show application VoiceMail"
# Expect: a description of the VoiceMail application.
# If you see "not registered", the module still failed to load — check
# `sudo asterisk -rx "module show like voicemail"` and journalctl -xeu asterisk.




2. Asterisk — PJSIP Trunk Config (Zadarma)


I should put on this place, becouse .env file not exucute on asterisk conf about specifics
This config have to put on:

/etc/asterisk/pjsip.conf


; ZADARMA
[zadarma]
type=registration
transport=transport-udp
outbound_auth=zadarma-auth
server_uri=sip:sip.zadarma.com
client_uri=sip:SIP_LOGIN@sip.zadarma.com
retry_interval=60
expiration=120
contact_user=SIP_LOGIN

[zadarma-auth]
type=auth
auth_type=userpass
username=SIP_LOGIN
password=SIP_PASSWORD

[zadarma]
type=aor
contact=sip:sip.zadarma.com

[zadarma]
type=endpoint
transport=transport-udp
context=zadarma-in
disallow=all
allow=alaw
allow=ulaw
outbound_auth=zadarma-auth
aors=zadarma
from_user=SIP_LOGIN
from_domain=sip.zadarma.com
direct_media=no

[zadarma]
type=identify
endpoint=zadarma
match=sip.zadarma.com

Apply and verify:

sudo asterisk -rx "pjsip reload"
sudo asterisk -rx "pjsip show registrations"
sudo asterisk -rx "pjsip show endpoint zadarma"

3. Asterisk — Dialplan Context

File: /etc/asterisk/extensions.conf, context [internal], must contain:
Activate venv & run FastAPI server

exten => _+380.,1,NoOp(Outgoing call via Zadarma: ${EXTEN})
 same => n,Dial(PJSIP/${EXTEN}@zadarma,60)
 same => n,Hangup()



4. .env (never commit this — see §7):

GMAIL_USER=YOUR_GMAIL@gmail.com
GMAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx
ALERT_EMAIL_TO=YOUR_GMAIL@gmail.com
ALERT_PHONE=YOUR_NUMBER



5. 9. Networking / Firewall
SIP signaling: UDP 5060 open to Zadarma's SIP servers
RTP media: open the RTP port range Asterisk uses (check rtp.conf, typically UDP 10000–20000)
If the server is behind NAT, set external_media_address / external_signaling_address / local_net in the [transport-udp] section of pjsip.conf
FastAPI's /alert endpoint (port 8000) should be reachable only from 127.0.0.1 (Alertmanager) — do not expose it publicly without authentication





6. Activate FastAPI
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000




