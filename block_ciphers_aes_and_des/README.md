# Block Ciphers, AES and Integrity

**Course:** CSC 3114: Cryptology and Coding Theory
**Assignment:** Take-Home Assignment (Test 2)
**Due:** 7 October 2026, 11:59 PM EAT

## Description

This assignment looks at how block ciphers like DES and AES work, and why integrity checks are needed on top of them. We:

- answer theory questions on confusion, diffusion and the avalanche effect, compare DES and AES, and compare the ECB, CBC and CTR modes;
- measure the avalanche effect of AES-128 in Python;
- encrypt and decrypt a message with AES-CBC and AES-CTR;
- show how tampering affects a SHA-256 hash and an HMAC-SHA256 tag;
- write a short reflection and record a group video (5 minutes or less).

The full brief is in [Takehome_assignment_Cryptology.pdf](Takehome_assignment_Cryptology.pdf).

## Group Members

| # | Name | Registration No. |
|---|------|------------------|
| 1 | [Name] | [Registration Number] |
| 2 | [Name] | [Registration Number] |
| 3 | [Name] | [Registration Number] |

## Task Ownership

| Member | Tasks | Folder(s) |
|--------|-------|-----------|
| Member 1: [Name / Registration Number] | Task 1 (Theory) + Task 2 (Avalanche) | `task1_theory/`, `task2_avalanche/` |
| Member 2: [Name / Registration Number] | Task 3 (AES Modes) | `task3_aes_modes/` |
| Member 3: [Name / Registration Number] | Task 4 (Integrity) + Task 5 (Reflection & Video) | `task4_integrity/`, `task5_reflection/` |

Everyone appears in the video and reviews the final PDF.

## Setup

You need Python 3.10 or newer.

```bash
# from inside this folder
python -m venv venv

# activate the virtual environment
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (Git Bash):
source venv/Scripts/activate
# macOS / Linux:
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Experiments

```bash
python task2_avalanche/avalanche.py
python task3_aes_modes/aes_modes.py
python task4_integrity/integrity.py
```

Save each script's output in `results/` and its screenshots in `screenshots/`.

## Task Checklist

- [ ] Task 1: Theory answers (a, b, c)
- [ ] Task 2: Avalanche experiment code
- [ ] Task 2: Results table, average and interpretation
- [ ] Task 3: CBC and CTR code
- [ ] Task 3: IV/nonce, ciphertext lengths and observations
- [ ] Task 4: Hash/HMAC code
- [ ] Task 4: Tampering demo and explanation
- [ ] Task 5: Reflection (200 words or less)
- [ ] Task 5: Video recorded and uploaded (5 minutes or less, all members)
- [ ] Final PDF compiled, with the video link
- [ ] PDF submitted
