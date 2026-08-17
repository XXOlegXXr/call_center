from fastapi import FastAPI
import subprocess
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

GMAIL_USER = "oleghresko@gmail.com"
GMAIL_APP_PASSWORD = "jsgkbgreibgydsgsfdbfb"
ALERT_EMAIL_TO = "oleghresko2006@gmail.com"
PHONE = "+380980450537"


def make_call():
    clean_phone = PHONE.lstrip("+")
    dial_string = f"PJSIP/zadarma/sip:{clean_phone}@sip.zadarma.com"
    cmd = [
        "sudo", "asterisk", "-rx",
        f"channel originate {dial_string} extension {PHONE}@internal"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("ASTERISK OUTPUT:", result.stdout, result.stderr)
    return result.returncode == 0



def send_email_alert(alert_data):
    msg = MIMEText(f"Critical alert fired:\n{alert_data}")
    msg["Subject"] = "Critical Alert — Call Center Monitoring"
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_EMAIL_TO
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, [ALERT_EMAIL_TO], msg.as_string())
        return True
    except Exception as e:
        print("EMAIL ERROR:", e)
        return False


@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/alert")
def alert(data: dict):
    for a in data.get("alerts", []):
        status = a.get("status")
        severity = a.get("labels", {}).get("severity")
        print(f"ALERT: status={status}, severity={severity}")
        if status == "firing" and severity == "critical":
            make_call()
            send_email_alert(a)
    return {"status": "received"}
