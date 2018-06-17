FROM phusion/baseimage:0.10.1

RUN apt-get update
RUN apt-get install -y python2.7
RUN apt-get install socat

ADD flag.py /hm4c/flag.py
ADD hm4c.py /hm4c/hm4c.py

EXPOSE 31337

CMD ["socat", "tcp-l:31337,crlf,fork", "system:'python2.7 /hm4c/hm4c.py'" ]
