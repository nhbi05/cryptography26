# Task 3: AES Modes in Practice (10 marks)

**Owner:** Member 2: [Name / Registration Number]

## What to do

Using a standard Python cryptographic library, with a message of at least 40 characters:

1. Encrypt and decrypt it with AES-CBC, using a fresh IV and correct padding.
2. Encrypt and decrypt it with AES-CTR, using a fresh nonce/counter.
3. Verify that the recovered plaintext exactly matches the original.
4. Report the IV/nonce in hex, the ciphertext length, and two observations comparing CBC and CTR.

## Library used

- **[`cryptography`](https://cryptography.io/)** (PyCA), version 46.0.3, the standard Python cryptographic library.
  - `Cipher`, `algorithms.AES`, `modes.CBC` and `modes.CTR` from `cryptography.hazmat.primitives.ciphers` run AES in each mode.
  - `padding.PKCS7` from `cryptography.hazmat.primitives` adds and removes the CBC padding.
- **`os.urandom`** (Python standard library) generates the key, IV and nonce with a cryptographically secure random generator.

Install with:

```bash
pip install -r requirements.txt
```

## How to run

```bash
python task3_aes_modes/aes_modes.py
```

## Setup

- **Message:** `The quick brown fox jumps over the lazy dog!!` (45 characters / 45 bytes)
- **Key:** AES-256 (32 random bytes, freshly generated each run)
- **CBC IV:** 16 random bytes, fresh for every encryption; PKCS7 padding
- **CTR nonce/counter:** 16 random bytes (initial counter block), fresh for every encryption; no padding

## Results

Values from one run. The key, IV and nonce are random, so the hex values differ on every run, but the lengths stay the same.

| | CBC | CTR |
|---|-----|-----|
| IV / nonce (hex) | `1815fd42b21b535d6ad86deee578d97c` | `a78ccd7e4320aba0727873a4affa64b1` |
| Plaintext length (bytes) | 45 | 45 |
| Ciphertext length (bytes) | 48 | 45 |
| Plaintext recovered exactly? | Yes | Yes |

Full ciphertexts from the same run:

- **CBC:** `d559cb1372e00560df48f0df61676b3a70f3425ea08a84040387c680e90ff1902d303cdc9d69401269a47fb84d1a7d6c`
- **CTR:** `a7033eb1cb96fe633ae95a07015444159ac15919ae31e111e26bbefa3ca17b9306b93bac63054d888f6bb9e136`

The script checks each recovered plaintext against the original with `==` and stops with an error if either does not match exactly. Both passed.

## Observations (CBC vs CTR)

1. **Padding and ciphertext length.** CBC works on whole 16-byte blocks, so the 45-byte message was PKCS7-padded to 48 bytes (3 blocks), and the ciphertext is longer than the plaintext. PKCS7 always adds at least one byte, so a message that is already a multiple of 16 grows by a full extra block. CTR turns AES into a stream cipher: it encrypts the nonce/counter to make a keystream and XORs it with the plaintext. It needs no padding, so the ciphertext is exactly 45 bytes, the same as the plaintext.

2. **Parallelism.** In CBC each plaintext block is XORed with the previous ciphertext block before encryption, so encryption is sequential: block *n* cannot be encrypted until block *n−1* is done. (CBC decryption can run in parallel, because all the ciphertext blocks are already known.) In CTR each block uses its own counter value, so every block is independent: both encryption and decryption can run in parallel, and you can jump straight to any block and decrypt it on its own.

3. **IV/nonce reuse.** Reusing a CTR nonce with the same key is catastrophic. It produces the same keystream, so XORing the two ciphertexts cancels the keystream and leaves the XOR of the two plaintexts. If either plaintext is known or guessable, the other is revealed. Reusing a CBC IV is also wrong but milder: identical messages give identical ciphertexts, and it reveals whether two messages start with the same blocks. That is why both modes here use a fresh random IV/nonce on every encryption.

4. **Error propagation.** Flipping one bit in a CBC ciphertext block garbles that whole 16-byte plaintext block when decrypted, and flips the same bit in the next plaintext block, because each ciphertext block feeds into decrypting the next. In CTR, flipping one ciphertext bit flips exactly one plaintext bit and nothing else, because each byte is just XORed with the keystream. This also means an attacker can make precise, predictable changes to a CTR plaintext without knowing the key.

Neither mode provides integrity: an attacker can modify the ciphertext without detection. Integrity is covered in Task 4.
