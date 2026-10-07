# Task 5: Reflection and Video Presentation (4 marks)

**Owner:** SUUNA RAYMOND (24/U/11403/EVE)

## Reflection (200 words or less)

What is the most important security lesson our group learned from the experiments?

The most important lesson we learned is that a strong cipher does not make a system secure on its own. How it is used matters just as much.

Our avalanche experiment showed that AES itself is very strong. Flipping a single plaintext bit changed 49.9% of the ciphertext bits on average, almost exactly the ideal 50%. But Task 3 showed that this strength depends on correct use. AES-CBC and AES-CTR both recovered our message exactly, and each encryption used a fresh random IV or nonce, so the same message never produced the same ciphertext. Reusing a CTR nonce with the same key would reveal the XOR of two plaintexts without anyone breaking AES. We also saw that encryption only hides content. Neither mode detects a modified ciphertext, and CTR even lets an attacker flip chosen plaintext bits.

Task 4 completed the picture. An attacker defeated a plain SHA-256 hash simply by recomputing it, but HMAC-SHA256 rejected the tampered message because the attacker did not have the secret key.

Secure communication therefore needs confidentiality and integrity together, plus careful handling of keys, IVs and nonces. This is why authenticated encryption such as AES-GCM is preferred in practice.

_(196 words)_

## Video Presentation

- **Link:** https://drive.google.com/file/d/1TARreFrYcpibNIpK1Uo6iej6iJCPtoCY/view?usp=sharing
- **Length:** _TODO (5 minutes or less)_

### Requirements checklist

- [ ] All group members appear
- [ ] Shows evidence that the code runs
- [ ] Explains the security meaning of the results (not reading code line by line)
- [ ] Uploaded to a platform the lecturer can access
- [ ] Link tested and added to the final PDF
