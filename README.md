Start

||

voicemail





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
