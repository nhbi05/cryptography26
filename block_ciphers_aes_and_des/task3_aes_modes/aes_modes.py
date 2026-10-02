# Task 3: AES Modes in Practice (CBC and CTR)
# Owner: Member 2

# TODO: import os and what is needed from the cryptography library
#       (Cipher, algorithms, modes, padding)


# TODO: choose a message of at least 40 characters (as bytes)


def aes_cbc_encrypt(key: bytes, plaintext: bytes):
    # TODO: generate a fresh random IV
    # TODO: pad the plaintext to a multiple of the block size
    # TODO: encrypt with AES-CBC
    # TODO: return (iv, ciphertext)
    pass


def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes):
    # TODO: decrypt with AES-CBC using the same IV
    # TODO: remove the padding
    # TODO: return the plaintext
    pass


def aes_ctr_roundtrip(key: bytes, plaintext: bytes):
    # TODO: generate a fresh random nonce/counter
    # TODO: encrypt with AES-CTR
    # TODO: decrypt with AES-CTR using the same nonce
    # TODO: return evidence (nonce, ciphertext, recovered plaintext)
    pass


if __name__ == "__main__":
    # TODO: generate an AES key

    # TODO: run CBC encrypt + decrypt

    # TODO: run CTR encrypt + decrypt

    # TODO: verify that both recovered plaintexts exactly match the original

    # TODO: print the IV and nonce in hexadecimal

    # TODO: print the ciphertext length for CBC and for CTR
    pass
