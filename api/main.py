from fastapi import FastAPI
import socket

app = FastAPI()

AMI_HOST = "127.0.0.1"
AMI_PORT = 5038
AMI_USER = "alertapi"
AMI_SECRET = "pass1234"

PHONE = "+380980450537"


def ami_command(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    s.connect((AMI_HOST, AMI_PORT))

    login = (
        "Action: Login\r\n"
        f"Username: {AMI_USER}\r\n"
        f"Secret: {AMI_SECRET}\r\n"
        "Events: off\r\n"
        "\r\n"
    )

    s.sendall(login.encode())

    response = s.recv(4096).decode()
    print("AMI LOGIN:")
    print(response)

    originate = (
        "Action: Originate\r\n"
        "Channel: PJSIP/zadarma\r\n"
        "Context: alert-outgoing\r\n"
        f"Exten: {PHONE}\r\n"
        "Priority: 1\r\n"
        "CallerID: ALERT\r\n"
        "Timeout: 30000\r\n"
        "Async: true\r\n"
        "\r\n"
    )

    s.sendall(originate.encode())

    response = s.recv(4096).decode()

    print("AMI ORIGINATE:")
    print(response)

    s.close()

    return response


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/alert")
def alert(data: dict):

    print("ALERT RECEIVED")
    print(data)

    for alert_data in data.get("alerts", []):

        status = alert_data.get("status")
        severity = alert_data.get("labels", {}).get("severity")

        print(f"status={status}")
        print(f"severity={severity}")

        if status == "firing" and severity == "critical":
            ami_command("originate")

    return {"status": "received"}
