from Crypto.Cipher import AES


# --------------------------------------------------
# 1. AES-128 key
# AES-128 requires a 16-byte key
# --------------------------------------------------

key = b"1234567890abcdef"


# --------------------------------------------------
# 2. 16-byte plaintext
# --------------------------------------------------

plaintext = b"Sixteen byte txt"


# Check that the plaintext is exactly 16 bytes
print("Plaintext:", plaintext)
print("Plaintext length:", len(plaintext), "bytes")


# --------------------------------------------------
# 3. Encrypt one 16-byte block
# --------------------------------------------------

def encrypt_block(data: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


# --------------------------------------------------
# 4. Flip exactly one bit
# --------------------------------------------------

def flip_bit(data: bytes, bit_index: int) -> bytes:
    b = bytearray(data)

    byte_i, offset = divmod(bit_index, 8)

    b[byte_i] ^= (1 << offset)

    return bytes(b)


# --------------------------------------------------
# 5. Count how many ciphertext bits changed
# --------------------------------------------------

def count_changed_bits(x: bytes, y: bytes) -> int:
    return sum(
        (a ^ b).bit_count()
        for a, b in zip(x, y)
    )


# --------------------------------------------------
# 6. Perform one avalanche trial
# --------------------------------------------------

def avalanche_trial(encrypt_block, plaintext: bytes, bit_index: int):

    # Encrypt the original plaintext
    c1 = encrypt_block(plaintext)

    # Flip exactly one bit and encrypt again
    c2 = encrypt_block(
        flip_bit(plaintext, bit_index)
    )

    # Count changed ciphertext bits
    return count_changed_bits(c1, c2)


# --------------------------------------------------
# 7. Encrypt the original plaintext
# --------------------------------------------------

original_ciphertext = encrypt_block(plaintext)

print("\nOriginal ciphertext:")
print(original_ciphertext.hex())


# --------------------------------------------------
# 8. Run at least 10 different single-bit flips
# --------------------------------------------------

bit_positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

results = []


for bit_index in bit_positions:

    changed_bits = avalanche_trial(
        encrypt_block,
        plaintext,
        bit_index
    )

    percentage = (changed_bits / 128) * 100

    results.append(
        (bit_index, changed_bits, percentage)
    )


# --------------------------------------------------
# 9. Display the results
# --------------------------------------------------

print("\nAES-128 Avalanche Experiment")
print("-" * 50)

print(
    f"{'Bit Flipped':<15}"
    f"{'Changed Bits':<15}"
    f"{'Percentage':<15}"
)

for bit_index, changed_bits, percentage in results:

    print(
        f"{bit_index:<15}"
        f"{changed_bits:<15}"
        f"{percentage:.2f}%"
    )


# --------------------------------------------------
# 10. Calculate the average
# --------------------------------------------------

average_changed_bits = (
    sum(result[1] for result in results)
    / len(results)
)

average_percentage = (
    average_changed_bits / 128
) * 100


print("\nAverage changed ciphertext bits:",
      round(average_changed_bits, 2))

print("Average percentage of changed ciphertext bits:",
      round(average_percentage, 2), "%")