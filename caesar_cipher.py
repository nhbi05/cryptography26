"""Caesar Cipher: encrypt/decrypt text using a shift key."""


def caesar_encrypt(text, shift):
    result = []
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        elif char.islower():
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def main():
    print("Caesar Cipher")
    text = input("Enter text: ")
    shift = int(input("Enter shift/key: "))
    choice = input("Encrypt or Decrypt? (e/d): ").strip().lower()

    if choice == 'e':
        print("Encrypted text:", caesar_encrypt(text, shift))
    elif choice == 'd':
        print("Decrypted text:", caesar_decrypt(text, shift))
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
