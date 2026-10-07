# Task 3: AES Modes in Practice (CBC and CTR)



import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16  # AES block size in bytes (128 bits)

# Message of at least 40 characters (45 bytes, so CBC padding is visible)
MESSAGE = b"The quick brown fox jumps over the lazy dog!!"


def aes_cbc_encrypt(key: bytes, plaintext: bytes):
    # Fresh random IV for every encryption
    iv = os.urandom(BLOCK_SIZE)

    # PKCS7 pad the plaintext to a multiple of the block size
    padder = padding.PKCS7(BLOCK_SIZE * 8).padder()
    padded = padder.update(plaintext) + padder.finalize()

    # Encrypt with AES-CBC
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    return iv, ciphertext


def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes):
    # Decrypt with AES-CBC using the same IV
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove the PKCS7 padding
    unpadder = padding.PKCS7(BLOCK_SIZE * 8).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()

    return plaintext


def aes_ctr_roundtrip(key: bytes, plaintext: bytes):
    # Fresh random 16-byte initial counter block (nonce + counter)
    nonce = os.urandom(BLOCK_SIZE)

    # Encrypt with AES-CTR (no padding needed, it acts as a stream cipher)
    encryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Decrypt with AES-CTR using the same nonce
    decryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).decryptor()
    recovered = decryptor.update(ciphertext) + decryptor.finalize()

    return nonce, ciphertext, recovered


if __name__ == "__main__":
    # AES-256 key
    key = os.urandom(32)

    print("=" * 60)
    print("Task 3: AES Modes in Practice")
    print("=" * 60)
    print(f"Message           : {MESSAGE.decode()}")
    print(f"Message length    : {len(MESSAGE)} bytes")
    print(f"Key (hex)         : {key.hex()}")

    # CBC encrypt + decrypt
    iv, cbc_ct = aes_cbc_encrypt(key, MESSAGE)
    cbc_pt = aes_cbc_decrypt(key, iv, cbc_ct)
    cbc_ok = cbc_pt == MESSAGE

    print("\n--- AES-CBC ---")
    print(f"IV (hex)          : {iv.hex()}")
    print(f"Ciphertext (hex)  : {cbc_ct.hex()}")
    print(f"Ciphertext length : {len(cbc_ct)} bytes")
    print(f"Recovered         : {cbc_pt.decode()}")
    print(f"Exact match       : {cbc_ok}")

    # CTR encrypt + decrypt
    nonce, ctr_ct, ctr_pt = aes_ctr_roundtrip(key, MESSAGE)
    ctr_ok = ctr_pt == MESSAGE

    print("\n--- AES-CTR ---")
    print(f"Nonce (hex)       : {nonce.hex()}")
    print(f"Ciphertext (hex)  : {ctr_ct.hex()}")
    print(f"Ciphertext length : {len(ctr_ct)} bytes")
    print(f"Recovered         : {ctr_pt.decode()}")
    print(f"Exact match       : {ctr_ok}")

    # Verify both recovered plaintexts exactly match the original
    assert cbc_ok, "CBC round trip failed"
    assert ctr_ok, "CTR round trip failed"

    print("\n--- Summary ---")
    print(f"CBC ciphertext length: {len(cbc_ct)} bytes "
          f"(padded from {len(MESSAGE)} to a multiple of {BLOCK_SIZE})")
    print(f"CTR ciphertext length: {len(ctr_ct)} bytes "
          f"(same as plaintext, no padding)")
    print("Both plaintexts recovered exactly: PASS")
