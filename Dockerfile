FROM alpine:3.7

RUN apk add --no-cache python socat

ADD flag.py /hm4c/flag.py
ADD hm4c.py /hm4c/hm4c.py

EXPOSE 31337

ENTRYPOINT ["socat", "tcp-l:31337,crlf,fork", "system:'python2.7 /hm4c/hm4c.py'" ]
