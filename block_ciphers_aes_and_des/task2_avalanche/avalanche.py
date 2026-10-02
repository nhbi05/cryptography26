# Task 2: AES-128 Avalanche Experiment
# Owner: Member 1

# TODO: import what is needed from the cryptography library (Cipher, algorithms, modes)


# TODO 1: Create an AES-128 key (16 bytes)

# TODO 2: Define a 16-byte plaintext


# Helper functions suggested in the assignment brief

def encrypt_block(block: bytes) -> bytes:
    # TODO: encrypt one 16-byte block with AES-128 and return the ciphertext
    pass


def flip_bit(data: bytes, bit_index: int) -> bytes:
    # TODO: return a copy of data with exactly one bit flipped
    pass


def count_changed_bits(x: bytes, y: bytes) -> int:
    # TODO: count how many bits differ between x and y
    pass


def avalanche_trial(encrypt_block, plaintext: bytes, bit_index: int):
    # TODO: encrypt the original, encrypt the bit-flipped version,
    #       and return the number of changed ciphertext bits
    pass


if __name__ == "__main__":
    # TODO 3: Encrypt the original plaintext

    # TODO 4: Choose at least 10 different bit positions to flip

    # TODO 5: Encrypt each modified plaintext

    # TODO 6: Count the changed ciphertext bits for each trial

    # TODO 7: Run at least 10 trials

    # TODO 8: Calculate the average percentage of changed bits

    # TODO 9: Display the results as a table
    pass
