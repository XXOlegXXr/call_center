from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Alert(BaseModel):
    severity: str
    message: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "asterisk-alert-api"
    }


@app.post("/alert")
def receive_alert(alert: Alert):
    print(f"[{alert.severity}] {alert.message}")

    return {
        "status": "received",
        "severity": alert.severity,
        "message": alert.message
    }
