import os, re
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse

app = FastAPI()

ALLOWED = {k.strip() for k in os.environ.get("ALLOWED_KEYS", "").split(",") if k.strip()}
DEBUG = os.environ.get("AUTHZ_DEBUG", "false").lower() == "true"

CRED_RE = re.compile(r"Credential=([A-Z0-9]{16,32})/")

Q_CRED_RE = re.compile(r"(?:^|[?&])X-Amz-Credential=([^&]+)")

def url_decode(s: str) -> str:
    try:
        from urllib.parse import unquote
        return unquote(s)
    except Exception:
        return s

def extract_access_key(req: Request) -> str | None:
    # try auth header
    auth = req.headers.get("authorization") or req.headers.get("Authorization")
    if auth:
        m = CRED_RE.search(auth)
        if m:
            return m.group(1)

    # try presigned url query
    qs = str(req.url.query or "")
    if qs:
        m2 = Q_CRED_RE.search(qs)
        if m2:
            raw = url_decode(m2.group(1))
            return raw.split("/", 1)[0]

    # try X-Amz-Access-Key header if present
    maybe = req.headers.get("X-Amz-Access-Key") or req.headers.get("x-amz-access-key")
    if maybe and re.fullmatch(r"[A-Z0-9]{16,32}", maybe):
        return maybe

    return None

@app.api_route("/authz", methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]) 
async def authz(request: Request):
    akid = extract_access_key(request)

    if DEBUG:
        print(f"[authz] URI={request.url.path}?{request.url.query} AKID={akid}")

    if not akid:
        return PlainTextResponse("Missing or unparsable credentials", status_code=403)

    if akid in ALLOWED:
        return PlainTextResponse("OK", status_code=200)

    return PlainTextResponse(f"Access key not allowed: {akid}", status_code=403)

