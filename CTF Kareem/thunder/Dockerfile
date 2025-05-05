# FROM alpine:3.16.0

# ARG DEBIAN_FRONTEND=noninteractive
# WORKDIR /app/
# RUN apk add socat python3 py-pip
# RUN python3 -m pip install pycryptodome
# COPY ./src/ /app/
# RUN addgroup -S ctf && \
#     adduser -S player -G ctf && \
#     chmod u+s /app/thunder.py

# RUN chown player:ctf /app/*
# USER player
# EXPOSE 1337
# ENTRYPOINT ["python3", "/app/thunder.py"]