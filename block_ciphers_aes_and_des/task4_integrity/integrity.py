# Task 4: Integrity and Tampering (SHA-256 and HMAC-SHA256)
# Owner: Member 3

# TODO: import hashlib, hmac (and os for generating a secret key)


# TODO: choose the original message (as bytes)

# TODO: create a modified copy of the message with exactly ONE character changed


def sha256_digest(message: bytes) -> str:
    # TODO: return the SHA-256 hex digest of the message
    pass


def make_hmac(key: bytes, message: bytes) -> bytes:
    # TODO: return the HMAC-SHA256 tag of the message
    pass


def verify_hmac(key: bytes, message: bytes, tag: bytes) -> bool:
    # TODO: recompute the tag and compare it safely with hmac.compare_digest
    pass


if __name__ == "__main__":
    # TODO: generate a secret HMAC key

    # TODO: compute the SHA-256 digest of the original message

    # TODO: compute the HMAC-SHA256 tag of the original message

    # TODO: recompute the SHA-256 digest and HMAC tag of the modified message

    # TODO: show how the digest and tag change after tampering

    # TODO: verify the HMAC for the original message (should pass)

    # TODO: verify the original tag against the modified message (should fail)
    pass
