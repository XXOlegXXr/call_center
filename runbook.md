DELETE CONFLICT MODULE ON DISC


sudo mkdir -p /root/asterisk-modules-disabled
sudo mv /usr/lib/x86_64-linux-gnu/asterisk/modules/app_voicemail_imap.so /root/asterisk-modules-disabled/
sudo mv /usr/lib/x86_64-linux-gnu/asterisk/modules/app_voicemail_odbc.so /root/asterisk-modules-disabled/




FULL RESTART ASTERISK AND WAIT


sudo systemctl restart asterisk
sleep 3


REVIEW

sudo asterisk -rx "core show application VoiceMail"
MAY SHOW DESKCIPTION(not ERRROR "not registered")

TEST


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
