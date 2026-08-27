"""Reverse Cipher: encrypt/decrypt text by reversing its characters.

Encryption and decryption are the same operation: reverse the string.
No key/shift is needed — reversing twice restores the original text.
"""


def reverse_encrypt(text):
    result = []
    for i in range(len(text) - 1, -1, -1):
        result.append(text[i])
    return "".join(result)


def reverse_decrypt(text):
    # Decrypting a reverse cipher is the same as encrypting it:
    # reverse the text again to get the original.
    return reverse_encrypt(text)


def main():
    print("Reverse Cipher")
    text = input("Enter text: ")
    choice = input("Encrypt or Decrypt? (e/d): ").strip().lower()

    if choice == "e":
        print("Encrypted text:", reverse_encrypt(text))
    elif choice == "d":
        print("Decrypted text:", reverse_decrypt(text))
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
