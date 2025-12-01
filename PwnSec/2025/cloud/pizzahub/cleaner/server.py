#!/usr/bin/env python3
import boto3
import botocore
import logging
import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ---- CONFIG ----
PREFIX = os.getenv("PREFIX", "blvkrose")
INTERVAL = int(os.getenv("INTERVAL_SECONDS", "300"))  # 5 minutes
HEALTH_PORT = int(os.getenv("HEALTH_PORT", "8080"))
AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("cleaner")

lambda_client = boto3.client(
    "lambda",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localstack:4566"),
    region_name=AWS_REGION
)

# ---- HEALTH SERVER ----
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok\n")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        return

def run_health_server(port):
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    log.info(f"Health server running on :{port}")
    server.serve_forever()

# ---- CLEANUP LOGIC ----
def list_all_functions():
    paginator = lambda_client.get_paginator("list_functions")
    for page in paginator.paginate():
        for fn in page.get("Functions", []):
            yield fn

def delete_function(fn_name):
    try:
        lambda_client.delete_function(FunctionName=fn_name)
        log.info(f"Deleted function: {fn_name}")
    except botocore.exceptions.ClientError as e:
        log.error(f"Failed to delete {fn_name}: {e}")

def cleanup_once():
    log.info("Cleanup cycle started")
    try:
        for fn in list_all_functions():
            name = fn.get("FunctionName")
            if not name:
                continue
            if name.startswith(PREFIX):
                delete_function(name)
    except Exception as e:
        log.exception(f"Cleanup run error: {e}")
    log.info("Cleanup cycle completed")

def main():
    threading.Thread(target=run_health_server, args=(HEALTH_PORT,), daemon=True).start()
    log.info(f"Cleaner started. Checking every {INTERVAL}s for prefix '{PREFIX}'")

    while True:
        cleanup_once()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

