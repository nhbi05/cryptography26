# Task 4: Integrity and Tampering (6 marks)

**Owner:** Member 3: [Name / Registration Number]

## What to do

Compute a SHA-256 hash and an HMAC-SHA256 tag for the message. Change one character and recompute both. Demonstrate:

- how the digest/tag changes after tampering;
- successful HMAC verification for the original message;
- failed verification for the modified message;
- why a plain hash does not authenticate the sender, while HMAC provides integrity and authentication using a secret key.

## How to run

```bash
python task4_integrity/integrity.py
```

## Results

_TODO: fill in from the actual run._

| | Original message | Modified message |
|---|------------------|------------------|
| SHA-256 | | |
| HMAC-SHA256 | | |
| HMAC verification | | |

## Why a hash alone is not enough

_TODO_
