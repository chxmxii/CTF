FROM oowy/opentofu:latest
RUN apk add go socat
WORKDIR /home/challenger
RUN adduser -D challenger
USER challenger
ENV TF_VAR_FLAG="Securinets{scuzabizzcuzza}}"
COPY entrypoint.sh .
COPY terraform-challenge .
COPY main .
COPY exec.sh .
RUN tofu init && tofu apply -auto-approve
ENTRYPOINT ["sh", "exec.sh"]
