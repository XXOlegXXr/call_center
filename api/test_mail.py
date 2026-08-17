import smtplib
from email.mime.text import MIMEText

GMAIL_USER = "oleghresko@gmail.com"
GMAIL_APP_PASSWORD = "16th_number_gmail_app_pass"
ALERT_EMAIL_TO = "oleghresko2006@gmail.com"

def send_email_alert():
    msg = MIMEText("Привіт! Це локальний тест відправки пошти.")
    msg["Subject"] = "Локальний тест Gmail SMTP"
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_EMAIL_TO
    
    try:
        print("Підключення до smtp.gmail.com...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()             
            print("Авторизація...")
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            print("Надсилання листа...")
            server.sendmail(GMAIL_USER, [ALERT_EMAIL_TO], msg.as_string())
        print("УСПІХ! Лист надіслано.")
        return True
    except Exception as e:
        print("ПОМИЛКА:", e)
        return False

if __name__ == "__main__":
    send_email_alert()
