# Cryptography Group Assignments

**Course:** CSC 3114: Cryptology and Coding Theory

This repository holds our group's practical work for CSC 3114. Each assignment has its own folder with its own README, which covers the details, group members and run instructions.

## Assignments

| Folder | Assignment | Status |
|--------|------------|--------|
| [ciphers_implemetation/](ciphers_implemetation/) | Classical ciphers: Caesar, Reverse and Vernam (encrypt/decrypt in Python) | Done |
| [block_ciphers_aes_and_des/](block_ciphers_aes_and_des/) | Take-Home Assignment (Test 2): Block ciphers, AES modes, avalanche effect, and integrity (SHA-256 / HMAC) | In progress |

## Requirements

- Python 3.10 or newer
- Some assignments need extra packages. If a folder has a `requirements.txt`, install them from inside that folder:

```bash
pip install -r requirements.txt
```

## Getting Started

```bash
git clone https://github.com/nhbi05/cryptography26.git
cd cryptography26
```

Then go into an assignment folder and follow its README.

## Working Together

- Pull before you start working: `git pull`
- Commit only your own task's files, with a clear message
- Don't commit virtual environments, `__pycache__/`, or secret keys
