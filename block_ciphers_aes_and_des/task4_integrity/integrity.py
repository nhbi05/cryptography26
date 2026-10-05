# Task 4: Integrity and Tampering (SHA-256 and HMAC-SHA256)
# Owner: Member 3

import hashlib
import hmac
import os

# Same message as Task 3
MESSAGE = b"The quick brown fox jumps over the lazy dog!!"

# Tampered copy with exactly ONE character changed ("fox" -> "box")
TAMPER_INDEX = MESSAGE.index(b"fox")
MODIFIED = MESSAGE[:TAMPER_INDEX] + b"b" + MESSAGE[TAMPER_INDEX + 1:]


def sha256_digest(message: bytes) -> str:
    return hashlib.sha256(message).hexdigest()


def make_hmac(key: bytes, message: bytes) -> bytes:
    return hmac.new(key, message, hashlib.sha256).digest()


def verify_hmac(key: bytes, message: bytes, tag: bytes) -> bool:
    # Recompute the tag and compare in constant time
    expected = make_hmac(key, message)
    return hmac.compare_digest(expected, tag)


def count_changed_bits(x: bytes, y: bytes) -> int:
    return sum((a ^ b).bit_count() for a, b in zip(x, y))


if __name__ == "__main__":
    # Secret key shared only by the sender and the receiver
    key = os.urandom(32)

    print("=" * 60)
    print("Task 4: Integrity and Tampering")
    print("=" * 60)
    print(f"Original message  : {MESSAGE.decode()}")
    print(f"Modified message  : {MODIFIED.decode()}")
    print(f"Changed position  : index {TAMPER_INDEX} "
          f"('{chr(MESSAGE[TAMPER_INDEX])}' -> '{chr(MODIFIED[TAMPER_INDEX])}')")
    print(f"HMAC key (hex)    : {key.hex()}")

    # Digest and tag of the original message
    orig_hash = sha256_digest(MESSAGE)
    orig_tag = make_hmac(key, MESSAGE)

    # Digest and tag of the modified message
    mod_hash = sha256_digest(MODIFIED)
    mod_tag = make_hmac(key, MODIFIED)

    # How the digest and tag change after tampering
    hash_bits = count_changed_bits(bytes.fromhex(orig_hash), bytes.fromhex(mod_hash))
    tag_bits = count_changed_bits(orig_tag, mod_tag)

    print("\n--- SHA-256 ---")
    print(f"Original          : {orig_hash}")
    print(f"Modified          : {mod_hash}")
    print(f"Bits changed      : {hash_bits}/256 ({hash_bits / 256:.2%})")

    print("\n--- HMAC-SHA256 ---")
    print(f"Original tag      : {orig_tag.hex()}")
    print(f"Modified tag      : {mod_tag.hex()}")
    print(f"Bits changed      : {tag_bits}/256 ({tag_bits / 256:.2%})")

    # Receiver checks the original message against the original tag
    ok_original = verify_hmac(key, MESSAGE, orig_tag)
    # Receiver checks the tampered message against the original tag
    ok_modified = verify_hmac(key, MODIFIED, orig_tag)

    print("\n--- HMAC verification (receiver holds the key) ---")
    print(f"Original message + original tag : {'PASS' if ok_original else 'FAIL'}")
    print(f"Modified message + original tag : {'PASS' if ok_modified else 'FAIL'}")

    # Why a plain hash does not authenticate the sender:
    # an attacker who changes the message can simply recompute SHA-256,
    # because SHA-256 needs no secret. The receiver's hash check then passes.
    forged_hash = sha256_digest(MODIFIED)
    # Receiver hashes what arrived and compares it with the attached hash
    hash_check = sha256_digest(MODIFIED) == forged_hash

    # The attacker cannot do the same with HMAC: without the secret key,
    # any tag they make (here, with a guessed key) fails verification.
    attacker_key = os.urandom(32)
    forged_tag = make_hmac(attacker_key, MODIFIED)
    forged_ok = verify_hmac(key, MODIFIED, forged_tag)

    print("\n--- Attacker modifies the message and replaces the checksum ---")
    print(f"Attacker's SHA-256  : {forged_hash}")
    print(f"Receiver hash check : {'PASS (tampering NOT detected)' if hash_check else 'FAIL'}")
    print(f"Attacker's HMAC tag : {forged_tag.hex()}")
    print(f"Receiver HMAC check : {'PASS' if forged_ok else 'FAIL (tampering detected)'}")

    assert orig_hash != mod_hash, "SHA-256 digest did not change"
    assert orig_tag != mod_tag, "HMAC tag did not change"
    assert ok_original, "HMAC should verify for the original message"
    assert not ok_modified, "HMAC should fail for the modified message"
    assert hash_check, "Recomputed plain hash should match"
    assert not forged_ok, "Forged HMAC should fail without the key"

    print("\n--- Summary ---")
    print("One changed character changes about half the bits of both outputs.")
    print("HMAC verifies the original message and rejects the modified one.")
    print("A plain hash can be recomputed by anyone, so it cannot prove who")
    print("sent the message. HMAC needs the secret key, so only a key holder")
    print("can produce a valid tag: it gives integrity AND authentication.")
