# Task 2: Python Avalanche Experiment (10 marks)

**Owner:** NABUKEERA SUMAYAH KASWA (24/U/07899/EVE)

## What to do

Use AES-128 to encrypt one 16-byte plaintext block. Flip exactly one bit in the plaintext, encrypt again with the same key, and count how many ciphertext bits change. Repeat for at least 10 different single-bit flips.

## How to run

```bash
python task2_avalanche/avalanche.py
```

## Setup

- **Key:** `1234567890abcdef` (AES-128, fixed so the results are reproducible)
- **Plaintext:** `Sixteen byte txt` (one 16-byte block)
- **Library:** PyCryptodome (`pip install pycryptodome`)

## Results

Full output in [`results/task2_avalanche_output.txt`](../results/task2_avalanche_output.txt).

| Trial | Bit flipped | Bits changed (out of 128) | % changed |
|-------|-------------|---------------------------|-----------|
| 1 | 0 | 59 | 46.09% |
| 2 | 1 | 63 | 49.22% |
| 3 | 2 | 59 | 46.09% |
| 4 | 3 | 68 | 53.12% |
| 5 | 4 | 73 | 57.03% |
| 6 | 5 | 64 | 50.00% |
| 7 | 6 | 64 | 50.00% |
| 8 | 7 | 59 | 46.09% |
| 9 | 8 | 66 | 51.56% |
| 10 | 9 | 64 | 50.00% |

**Average:** 63.9 of 128 bits changed (**49.92%**).

## Interpretation

Flipping one plaintext bit changed 49.92% of the ciphertext bits on average, very close to the ideal 50%. Every trial fell between 46.09% and 57.03%, so the behaviour is consistent across bit positions. This is the avalanche effect produced by AES's confusion and diffusion. The ciphertexts of two almost identical plaintexts look unrelated, so an attacker learns nothing about how similar the inputs were and cannot recover the key or plaintext by making small changes and watching the output.
