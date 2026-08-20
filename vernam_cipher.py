# Vernam Cipher

def vernam_encrypt(text, key):
    result = ""

    for i in range(len(text)):
        text_number = ord(text[i].upper()) - ord('A')
        key_number = ord(key[i].upper()) - ord('A')

        encrypted_number = text_number ^ key_number
        encrypted_number = encrypted_number % 26

        result += chr(encrypted_number + ord('A'))

    return result


def vernam_decrypt(ciphertext, key):
    result = ""

    for i in range(len(ciphertext)):
        cipher_number = ord(ciphertext[i].upper()) - ord('A')
        key_number = ord(key[i].upper()) - ord('A')

        original_number = cipher_number ^ key_number
        original_number = original_number % 26

        result += chr(original_number + ord('A'))

    return result


# Ask the user what they want to do
choice = input("Do you want to encrypt or decrypt? ").lower()

if choice == "encrypt":

    text = input("Enter the text: ")
    key = input("Enter the key: ")

    if len(text) != len(key):
        print("Error: The key must be the same length as the text.")
    else:
        result = vernam_encrypt(text, key)
        print("Encrypted text:", result)


elif choice == "decrypt":

    text = input("Enter the encrypted text: ")
    key = input("Enter the key: ")

    if len(text) != len(key):
        print("Error: The key must be the same length as the text.")
    else:
        result = vernam_decrypt(text, key)
        print("Decrypted text:", result)


else:
    print("Invalid choice.")