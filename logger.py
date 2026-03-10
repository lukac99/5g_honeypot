from fastapi import Request
from datetime import datetime, timezone
import json


async def log_request(request: Request):
    body = await request.body()

    log_entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "ip": request.client.host if request.client else "unknown",
        "method": request.method,
        "path": request.url.path,
        "query": dict(request.query_params), # /?target_nf_type=AMF -> {"target_nf_type": "AMF"}
        "headers": dict(request.headers),
        "body": body.decode("utf-8", errors="ignore") # dekodira iz bytes v string
    }

    with open("/app/logs/requests.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")  # prevedi dictionary v JSON zapis