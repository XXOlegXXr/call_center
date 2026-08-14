from panoramisk import Manager


manager = Manager(
    host="127.0.0.1",
    port=5038,
    username="alertapi",
    secret="pass1234",
)


async def call_extension(extension: str):
    await manager.connect()

    response = await manager.send_action({
        "Action": "Originate",
        "Channel": f"PJSIP/{extension}",
        "Context": "internal",
        "Exten": "1002",
        "Priority": 1,
        "CallerID": "ALERT",
        "Timeout": 30000,
        "Async": "true",
    })

    print(response)

    await manager.close()
