from fastapi import FastAPI
import subprocess

app = FastAPI()

PHONE = "+380980450537"


def make_call():
    cmd = [
        "sudo",
        "asterisk",
        "-rx",
        f"channel originate PJSIP/zadarma extension {PHONE}@alert-outgoing"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    print("ASTERISK:")
    print(result.stdout)
    print(result.stderr)

    return result.returncode == 0


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/alert")
def alert(data: dict):

    for alert in data.get("alerts", []):

        status = alert.get("status")
        severity = alert.get("labels", {}).get("severity")

        print(
            f"ALERT: status={status}, severity={severity}"
        )

        if status == "firing" and severity == "critical":
            make_call()

    return {"status": "received"}
