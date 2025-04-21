#!/usr/bin/env bash

set -euo pipefail

# Admin credentials (bootstrap user)
ADMIN_ENDPOINT="localhost:9000"
ADMIN_ACCESS_KEY="admin-access-key"
ADMIN_SECRET_KEY="admin-secret-key"
ADMIN_ALIAS="admin"

# User credentials (for uploading secret)
UPLOAD_USER_ALIAS="uploader"
UPLOAD_USERNAME="uploader-user"
UPLOAD_ACCESS_KEY="uploader-access-key"
UPLOAD_SECRET_KEY="uploader-secret-key"

# Common values
POLICY_NAME="upload-policy"
POLICY_FILE_PATH="./policy.json"
BUCKET_NAME="test-bucket"
FILE_TO_UPLOAD="./secret.txt"
OBJECT_NAME="secret.txt"

deploy_challenge() {
    docker compose up -d
}

create_minio_user_and_policy() {
    mc alias set "$ADMIN_ALIAS" "http://$ADMIN_ENDPOINT" "$ADMIN_ACCESS_KEY" "$ADMIN_SECRET_KEY"

    # Create user
    mc admin user add "$ADMIN_ALIAS" "$ add" "$UPLOAD_SECRET_KEY"

    # Create and attach policy
    mc admin policy create "$ADMIN_ALIAS" "$POLICY_NAME" "$POLICY_FILE_PATH"
    mc admin policy attach "$ADMIN_ALIAS" "$POLICY_NAME" --user="$UPLOAD_USERNAME"
}

put_secret() {
    # Login as uploader user
    mc alias set "$UPLOAD_USER_ALIAS" "http://$ADMIN_ENDPOINT" "$UPLOAD_USERNAME" "$UPLOAD_SECRET_KEY"

    # Create bucket and upload using the user (if bucket exists already, skip error)
    mc mb "$UPLOAD_USER_ALIAS/$BUCKET_NAME" || echo "Bucket $BUCKET_NAME already exists"
    mc version enable "$UPLOAD_USER_ALIAS/$BUCKET_NAME"
    mc cp "$FILE_TO_UPLOAD" "$UPLOAD_USER_ALIAS/$BUCKET_NAME/$OBJECT_NAME"
}

# Execute
deploy_challenge
create_minio_user_and_policy
put_secret
