#!/bin/sh
socat tcp-l:31337,crlf,fork system:'python2.7 /hm4c/hm4c.py'
