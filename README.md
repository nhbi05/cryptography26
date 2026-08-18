# Cryptography Assignment

Write a Python program to encrypt/decrypt a text given the key/shift using:

1. Caesar cipher
2. Reverse cipher
3. Vernam cipher

## Files

- [caesar_cipher.py](caesar_cipher.py) — Caesar cipher encrypt/decrypt
- `reverse_cipher.py` — Reverse cipher encrypt/decrypt
- `vernam_cipher.py` — Vernam cipher encrypt/decrypt

## Usage

### Caesar cipher

```
python caesar_cipher.py
```

You'll be prompted for:
- the text
- the shift/key (an integer)
- whether to encrypt (`e`) or decrypt (`d`)

Case is preserved and non-alphabetic characters (spaces, punctuation) are left unchanged.

Example:

```
Enter text: Hello, World!
Enter shift/key: 3
Encrypt or Decrypt? (e/d): e
Encrypted text: Khoor, Zruog!
```
