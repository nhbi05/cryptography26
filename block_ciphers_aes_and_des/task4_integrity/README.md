# Task 4: Integrity and Tampering (6 marks)

**Owner:** SUUNA RAYMOND (24/U/11403/EVE)

## What to do

Compute a SHA-256 hash and an HMAC-SHA256 tag for the message. Change one character and recompute both. Demonstrate:

- how the digest/tag changes after tampering;
- successful HMAC verification for the original message;
- failed verification for the modified message;
- why a plain hash does not authenticate the sender, while HMAC provides integrity and authentication using a secret key.

## Library used

Python standard library only, so there is nothing extra to install:

- **`hashlib.sha256`** computes the SHA-256 digest.
- **`hmac.new(key, message, hashlib.sha256)`** computes the HMAC-SHA256 tag.
- **`hmac.compare_digest`** compares tags in constant time, so the time taken does not leak how many leading bytes matched.
- **`os.urandom`** generates the 32-byte secret HMAC key.

## How to run

```bash
python task4_integrity/integrity.py
```

## Setup

- **Original message:** `The quick brown fox jumps over the lazy dog!!` (the same message as Task 3)
- **Modified message:** `The quick brown box jumps over the lazy dog!!` (one character changed: index 16, `f` → `b`)
- **HMAC key:** 32 random bytes, freshly generated each run

## Results

Values from one run (full output in [`results/task4_integrity_output.txt`](../results/task4_integrity_output.txt)). SHA-256 has no key, so its digests are the same on every run. The HMAC key is random, so the tags differ on every run, but the PASS/FAIL results stay the same.

| | Original message | Modified message |
|---|------------------|------------------|
| SHA-256 | `e8af66642705ee57fa03c5af5043d78260528448ec429b95e7c2547db1e3716d` | `a77516c3a66ba61957b0e691cbe3058dc88d393e904f735a3216eb9f7a66cf5a` |
| HMAC-SHA256 | `6c49e8a73508e7ebb8ae14aa22e03c69225a54759cf06363760a27190631e97b` | `5ef97473e043fdeb60a0f732449d9e107efe6165c042e6ef78245ab91ba1ed01` |
| HMAC verification (against the original tag) | PASS | FAIL |

**How much the outputs changed:** one changed character flipped 142 of 256 bits (55.5%) of the SHA-256 digest and 112 of 256 bits (43.8%) of the HMAC tag. The two digests look unrelated, so nobody can tell from the outputs how similar the two messages were. This is the avalanche effect again, as in Task 2.

## Why a hash alone is not enough

SHA-256 has no secret. Anyone can compute it, including an attacker. If a sender transmits `message + SHA-256(message)`, an attacker in the middle can change the message, recompute the SHA-256 of the new message, and replace the attached hash. The receiver hashes what arrived, gets a match, and accepts the forgery. The script shows this: the attacker's recomputed hash passes the receiver's check (**tampering NOT detected**). A plain hash only detects *accidental* corruption. It cannot show who sent the message.

HMAC mixes a secret key into the hash. Only someone who holds the key can produce a valid tag for a message. An attacker who changes the message cannot compute the matching tag. The script shows this: a tag made with any other key fails verification (**tampering detected**). So when the tag verifies, the receiver knows two things:

- **Integrity:** the message was not changed, because any change gives a completely different tag.
- **Authentication:** the message came from someone who holds the shared key.

HMAC does not provide non-repudiation. The sender and the receiver share the same key, so either one could have made the tag. A digital signature is needed to prove to a third party which one of them sent the message.
