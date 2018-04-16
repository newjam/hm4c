# hm4c

Solution to midnightsun 2018 qualifier ctf crypto challenge 'hm4c'

The `h4mc.py` service essentially accepts a `message` and returns

    sha256((key ⊕ message) + message)

Where ⊕ is bitwise XOR and `+` is bitwise addition

Suppose `key = 01100001` and our `message = 00000000`, then

     key                      = 01100001
     message                  = 00000000
     key ⊕ message            = 01100001
    (key ⊕ message) + message = 01100001

That is `(key ⊕ message) + message = key` 

So immediately we can get `sha256(key)`.
However, this is not particularly useful on it's own, as it would be computationally intractible to find the 'preimage' of the hash.

However suppose Suppose `key = 01100001` and our `message = 00000001`.
Notice how `message` matches `key` on the `0`th bit.
Then

     key                      = 01100001
     message                  = 00000001
     key ⊕ message            = 01100000
    (key ⊕ message) + message = 01100001

So because the `0`th bit `message` matched the `0`th bit of `key`, `(key ⊕ message) + message = key` again.

We now have the kernel of an algorithm for inferring `key` by testing the `i`th bit of `key`.
If the `sha256` of our test of the `i`th bit is equal to `sha256(key)`, we can infer that the `i`th bit of `key` is set.
Otherwise the `i`th bit of `key` is not set.

The exploiable flaw in the toy implementation of an 'HMAC' is that the `+` should be concatenation, not bitwise addition.

`hm4c_solution.py` connects to a `hm4c.py` service, either locally or remotely, and tests each bit until the entire `key` has been inferred.
