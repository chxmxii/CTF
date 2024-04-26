FROM golang:1.22.1 AS build
WORKDIR /app
COPY go.mod go.mod
COPY main.go main.go
RUN go mod download
COPY templates templates
COPY files/ddee01554441541102257 /etc/files/
COPY files/kc65334734942636999434734942 /tmp/
COPY images /images
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/openheimer
COPY files/build-file.txt /app/build-file.txt

FROM alpine:latest AS testing
WORKDIR /app
COPY files/p054derradasdgffas /var/file/
COPY --from=build /app/openheimer /app/openheimer
COPY --from=build /etc/files /etc/files
COPY --from=build /tmp /tmp
COPY files/e2ggar20125444egenv ~/random/
RUN rm -f /etc/files/* && rm -rf /tmp/*

FROM alpine:latest AS staging
WORKDIR /app
COPY files/qZaasd410ddacck /tmp/secreto/
COPY --from=build /app /app
copy --from=testing ~/random ~/random
COPY --from=testing /var/file /var/file
COPY files/f8224879845811005987100145g important/f8224879845811005987100145g
RUN rm -f /var/file/* && rm -rf ~/random

FROM alpine:latest AS prod
EXPOSE 8080
COPY --from=staging /app /app
COPY --from=staging /tmp /tmp
RUN rm -f /app/important/* && rm -rf /tmp/*

CMD [ "/app/openheimer" ]
