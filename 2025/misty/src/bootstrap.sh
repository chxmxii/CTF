#!/usr/bin/env bash

set -euo pipefail

# admin creds
ADMIN_ENDPOINT="localhost:9000"
ADMIN_ACCESS_KEY="admin-access-key"
ADMIN_SECRET_KEY="admin-secret-key"
ADMIN_ALIAS="admin"

# User credentials (for uploading secret)
UPLOAD_USER_ALIAS="mister07"
UPLOAD_USERNAME="mister07-usr"
UPLOAD_ACCESS_KEY="tbd"
UPLOAD_SECRET_KEY="tbd"

# Common values
POLICY_NAME="upload-policy"
POLICY_FILE_PATH="./policy.json"
BUCKET_NAME="test-bucket"
FILE_TO_UPLOAD="./secret.txt"
OBJECT_NAME="secret.txt"


function create_minio_user() {
    mc alias set "$ADMIN_ALIAS" "http://$ADMIN_ENDPOINT" "$ADMIN_ACCESS_KEY" "$ADMIN_SECRET_KEY"
    mc admin user add "$ADMIN_ALIAS" "$ add" "$UPLOAD_SECRET_KEY"
}

function create_and_attach_minio_policy() {
    mc admin policy create "$ADMIN_ALIAS" "$POLICY_NAME" "$POLICY_FILE_PATH"
    mc admin policy attach "$ADMIN_ALIAS" "$POLICY_NAME" --user="$UPLOAD_USERNAME"
}


function put_secret() {
    # Login as uploader user
    mc alias set "$UPLOAD_USER_ALIAS" "http://$ADMIN_ENDPOINT" "$UPLOAD_USERNAME" "$UPLOAD_SECRET_KEY"

    mc version enable "$UPLOAD_USER_ALIAS/$BUCKET_NAME"
    mc cp "$FILE_TO_UPLOAD" "$UPLOAD_USER_ALIAS/$BUCKET_NAME/$OBJECT_NAME"
}

function main() {
    create_minio_user()
    create_and_attach_minio_policy()
    put_secret()
}

main
