from pwn import process, remote, context, log
from base64 import b64encode
from hashlib import sha256
from string import printable
from functools import partial
from itertools import count, islice, izip, tee, takewhile, imap

def get_digest_from_tube(io, x):
  io.recvuntil('Quit')
  io.recvline()
  io.sendline('1')
  io.recvline()
  io.sendline(b64encode(x))
  return int(io.recvline())

def matches(get_digest): 
  # get the sha256 of the flag by digesting 0
  key_hash = get_digest('\x00')

  key = 0
  for i in count():
    # get sha256((flag ^ 2**i) + 2^i) from the server 
    digest = get_digest(from_int(2**i))
    # test if the ith bit is set in the flag and it to the key if it is
    if digest == key_hash:
      key = key ^ 2**i 
    # if we have tested a multiple of 8 bits, yield the answer so far
    if i % 8 == 0:
      yield from_int(key)

def main(): 
  log.info('Starting to pwn')
  #context.log_level = 'debug'
  #io = remote('crypto.midnightsunctf.se', 31337)
  io = remote('127.0.0.1', 31337)
  #io = process(['python',  'hm4c.py'])
  get_digest = partial(get_digest_from_tube, io)

  curr_i, prev_i = tee(matches(get_digest))
  prev_i         = islice(prev_i, 1, None)

  # keep printing the partial flag until we have found the entire flag
  progress = log.progress('Finding flag')
  for prev, curr in izip(curr_i, prev_i):
    if prev == curr:
      progress.success(curr)
      break
    else:
      progress.status(curr)


def from_int(i):
  ''' inverse of the to_int function on the server '''
  h = hex(i)[2:]
  h = h if len(h) % 2 == 0 else '0' + h
  return h.decode('hex')

if __name__ == "__main__":
  main()
