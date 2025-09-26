FROM registry.gitlab.com/qio/standard/python:3.10-alpine

RUN apk update && apk add --no-cache \
    bash \
    sudo \
    g++ \
    clang \
    build-base \
    openjdk17 \
    libc6-compat \
    && rm -rf /var/cache/apk/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /judge

RUN adduser -D -h /home/sandbox sandbox
USER sandbox

ENTRYPOINT ["tail", "-f", "/dev/null"]
