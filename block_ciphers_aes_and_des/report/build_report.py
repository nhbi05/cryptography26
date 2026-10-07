# Builds the group report (report.html and report.pdf) from the task folders.
# Code listings and program outputs are read straight from the repo, so the
# evidence in the PDF is always the real code and the real saved runs.
#
# Usage (from block_ciphers_aes_and_des/):
#   python report/build_report.py

import html
import shutil
import subprocess
from pathlib import Path

# ---------------------------------------------------------------
# Fill these in
# ---------------------------------------------------------------
GROUP = "Group 4"
MEMBERS = [
    # (name, registration number, student number, tasks)
    ("NANSEREKO HOUSNAH", "24/U/09631/EVE", "2400709631", "Task 3 (AES Modes)"),
    ("SUUNA RAYMOND", "24/U/11403/EVE", "2400711403", "Task 4 (Integrity), Task 5 (Reflection & Video)"),
    ("NABUKEERA SUMAYAH KASWA", "24/U/07899/EVE", "2400707899", "Task 1 (Theory), Task 2 (Avalanche)"),
]
VIDEO_LINK = "https://drive.google.com/file/d/1TARreFrYcpibNIpK1Uo6iej6iJCPtoCY/view?usp=sharing"

ROOT = Path(__file__).resolve().parent.parent
OUT_HTML = ROOT / "report" / "report.html"
OUT_PDF = ROOT / "report" / "report.pdf"
REFL_HTML = ROOT / "report" / "reflection.html"
REFL_PDF = ROOT / "report" / "reflection.pdf"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def pre(rel):
    return f'<pre class="code">{html.escape(read(rel).rstrip())}</pre>'


def mark(text):
    # Highlight anything still in [brackets] so missing details stand out
    if text.startswith("[") and text.endswith("]"):
        return f'<span class="todo">{html.escape(text)}</span>'
    return html.escape(text)


def find_browser():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    for name in ("msedge", "google-chrome", "chromium", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


# ---------------------------------------------------------------
# Results parsed from the saved runs
# ---------------------------------------------------------------
def task2_rows():
    rows = []
    for line in read("results/task2_avalanche_output.txt").splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0].isdigit() and parts[2].endswith("%"):
            rows.append(parts)
    return rows


def field(text, label):
    for line in text.splitlines():
        if line.startswith(label):
            return line.split(":", 1)[1].strip()
    raise ValueError(f"{label!r} not found")


t2 = task2_rows()
t2_avg_bits = sum(int(r[1]) for r in t2) / len(t2)
t2_avg_pct = t2_avg_bits / 128 * 100
t2_pcts = [float(r[2].rstrip("%")) for r in t2]

t3 = read("results/task3_aes_modes_output.txt")
cbc_part, ctr_part = t3.split("--- AES-CTR ---")
t3_msg = field(t3, "Message           ")
t3_cbc_iv = field(cbc_part, "IV (hex)")
t3_cbc_ct = field(cbc_part, "Ciphertext (hex)")
t3_cbc_len = field(cbc_part, "Ciphertext length")
t3_cbc_ok = field(cbc_part, "Exact match")
t3_ctr_nonce = field(ctr_part, "Nonce (hex)")
t3_ctr_ct = field(ctr_part, "Ciphertext (hex)")
t3_ctr_len = field(ctr_part, "Ciphertext length")
t3_ctr_ok = field(ctr_part, "Exact match")

t4 = read("results/task4_integrity_output.txt")
sha_part, rest = t4.split("--- HMAC-SHA256 ---")
hmac_part = rest.split("--- HMAC verification")[0]
t4_sha_o = field(sha_part, "Original          ")
t4_sha_m = field(sha_part, "Modified          ")
t4_sha_bits = field(sha_part, "Bits changed")
t4_tag_o = field(hmac_part, "Original tag")
t4_tag_m = field(hmac_part, "Modified tag")
t4_tag_bits = field(hmac_part, "Bits changed")

REFLECTION = """
<p>The most important lesson we learned is that a strong cipher does not make a
system secure on its own. How it is used matters just as much.</p>
<p>Our avalanche experiment showed that AES itself is very strong. Flipping a single
plaintext bit changed 49.9% of the ciphertext bits on average, almost exactly the ideal
50%. But Task 3 showed that this strength depends on correct use. AES-CBC and AES-CTR
both recovered our message exactly, and each encryption used a fresh random IV or nonce,
so the same message never produced the same ciphertext. Reusing a CTR nonce with the
same key would reveal the XOR of two plaintexts without anyone breaking AES. We also saw
that encryption only hides content. Neither mode detects a modified ciphertext, and CTR
even lets an attacker flip chosen plaintext bits.</p>
<p>Task 4 completed the picture. An attacker defeated a plain SHA-256 hash simply by
recomputing it, but HMAC-SHA256 rejected the tampered message because the attacker
did not have the secret key.</p>
<p>Secure communication therefore needs confidentiality and integrity together, plus
careful handling of keys, IVs and nonces. This is why authenticated encryption such as
AES-GCM is preferred in practice.</p>
"""

members_rows = "\n".join(
    f"<tr><td>{i}</td><td>{mark(n)}</td><td>{mark(r)}</td><td>{mark(sn)}</td><td>{html.escape(t)}</td></tr>"
    for i, (n, r, sn, t) in enumerate(MEMBERS, 1)
)
if VIDEO_LINK.startswith("http"):
    video_html = f'<a href="{html.escape(VIDEO_LINK)}">{html.escape(VIDEO_LINK)}</a>'
else:
    video_html = mark(VIDEO_LINK)

t2_table = "\n".join(
    f"<tr><td>{i}</td><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    for i, r in enumerate(t2, 1)
)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Block Ciphers, AES and Integrity: Group Report</title>
<style>
  @page {{ size: A4; margin: 18mm 17mm; }}
  body {{ font-family: "Times New Roman", Georgia, serif; font-size: 11.5pt;
         line-height: 1.45; color: #111; background: #fff; }}
  h1 {{ font-size: 20pt; margin: 0 0 4px; text-align: center; }}
  h2 {{ font-size: 14pt; color: #8b1a1a; border-bottom: 1px solid #8b1a1a;
        padding-bottom: 2px; margin-top: 22px; }}
  h3 {{ font-size: 12pt; margin: 14px 0 4px; }}
  .sub {{ text-align: center; margin: 0; }}
  .cover {{ margin-bottom: 18px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 10.5pt; }}
  th, td {{ border: 1px solid #555; padding: 4px 7px; text-align: left; vertical-align: top; }}
  th {{ background: #eee; }}
  code, .hex {{ font-family: Consolas, "Courier New", monospace; font-size: 9.5pt; }}
  .hex {{ word-break: break-all; }}
  h2, h3, h2 + p {{ break-after: avoid; }}
  pre.code, pre.out {{ font-family: Consolas, "Courier New", monospace; font-size: 8.3pt;
        line-height: 1.3; background: #f4f4f4; border: 1px solid #999; padding: 7px;
        white-space: pre-wrap; word-break: break-all; }}
  pre {{ break-inside: auto; }}
  .todo {{ background: #ffef9e; font-weight: bold; }}
  .pagebreak {{ break-before: page; }}
  .note {{ font-size: 10pt; color: #333; }}
</style>
</head>
<body>

<div class="cover">
<h1>Block Ciphers, AES and Integrity</h1>
<p class="sub"><b>CSC 3114: Cryptology and Coding Theory</b>, Take-Home Assignment (Test 2)</p>
<p class="sub">Submitted: 7 October 2026</p>

<h2>Group Members: {GROUP}</h2>
<table>
<tr><th>#</th><th>Name</th><th>Registration No.</th><th>Student No.</th><th>Tasks</th></tr>
{members_rows}
</table>

<p><b>Video presentation:</b> {video_html}</p>
<p><b>Language and libraries:</b> Python 3; PyCryptodome (Task 2), PyCA
<code>cryptography</code> (Task 3), and the standard library <code>hashlib</code>,
<code>hmac</code> and <code>os</code> (Task 4). Full code listings and program outputs
are in the Appendix.</p>
</div>

<h2>Task 1: Theory and Cipher Design</h2>

<h3>a) Confusion, diffusion and the avalanche effect</h3>
<p><b>Confusion</b> makes the relationship between the encryption key and the ciphertext
complex, so it is difficult for an attacker to work out the key from the ciphertext. In
AES, <b>SubBytes</b> provides confusion by replacing each byte using a non-linear
substitution table, the S-box.</p>
<p><b>Diffusion</b> spreads the effect of one plaintext bit across many ciphertext bits,
so patterns in the original message are hard to recognise. In AES, <b>ShiftRows</b> and
<b>MixColumns</b> provide diffusion by rearranging and mixing the data across the state.</p>
<p>The <b>avalanche effect</b> means that a small change in the input, such as one
plaintext bit, should change many bits of the ciphertext. AES achieves this through
repeated rounds of substitution, shifting, mixing and key addition. Ideally, changing one
bit changes about half of the ciphertext bits. Task 2 confirms this experimentally.</p>

<h3>b) DES vs AES</h3>
<table>
<tr><th>Property</th><th>DES</th><th>AES</th></tr>
<tr><td>Block size</td><td>64 bits</td><td>128 bits</td></tr>
<tr><td>Key size</td><td>56 effective bits (64 with parity)</td><td>128, 192 or 256 bits</td></tr>
<tr><td>Number of rounds</td><td>16</td><td>10, 12 or 14 (by key size)</td></tr>
<tr><td>Cipher structure</td><td>Feistel network</td><td>Substitution-permutation network</td></tr>
<tr><td>Present-day security</td><td>Insecure: the 56-bit key is too small and can be brute-forced</td>
    <td>Secure when properly implemented with an appropriate key size</td></tr>
</table>

<h3>c) ECB vs CBC vs CTR</h3>
<p><b>ECB (Electronic Codebook):</b> each plaintext block is encrypted independently, so
identical plaintext blocks give identical ciphertext blocks under the same key. This
reveals patterns, which makes ECB unsuitable for most applications.</p>
<p><b>CBC (Cipher Block Chaining):</b> each plaintext block is XORed with the previous
ciphertext block before encryption. CBC needs an IV so that identical plaintexts do not
produce identical ciphertexts, and it needs padding to fill whole blocks.</p>
<p><b>CTR (Counter):</b> AES encrypts a nonce and counter to produce a keystream, which is
XORed with the plaintext. It needs no padding and can encrypt data of any length.</p>
<p><b>Purpose of an IV/nonce:</b> it gives each encryption a fresh starting value, so
encrypting the same plaintext with the same key does not produce the same ciphertext.</p>
<p><b>Misuse to avoid:</b> a nonce must <b>never be reused with the same key in CTR
mode</b>. Reuse produces the same keystream and exposes the XOR of the plaintexts,
which seriously weakens security.</p>

<h2>Task 2: Python Avalanche Experiment</h2>
<p>Using AES-128 with a fixed key (<code>1234567890abcdef</code>), we encrypted the
16-byte block <code>Sixteen byte txt</code>. We then flipped one plaintext bit at a time
(bits 0 to 9), encrypted again with the same key, and counted the ciphertext bits that
changed out of 128.</p>
<table>
<tr><th>Trial</th><th>Bit flipped</th><th>Bits changed (of 128)</th><th>% changed</th></tr>
{t2_table}
<tr><th colspan="2">Average</th><th>{t2_avg_bits:.1f}</th><th>{t2_avg_pct:.2f}%</th></tr>
</table>
<p><b>Interpretation.</b> On average, flipping a single plaintext bit changed
<b>{t2_avg_bits:.1f} of 128 bits ({t2_avg_pct:.2f}%)</b>, very close to the ideal 50%.
Every trial fell between {min(t2_pcts):.2f}% and {max(t2_pcts):.2f}%, so the behaviour is
consistent and no bit position is weak. This is the avalanche effect produced by AES's
confusion and diffusion. For security, it means the ciphertexts of two almost identical
plaintexts look unrelated, so an attacker learns nothing about how similar the inputs
were and cannot recover the key or plaintext by making small changes and watching the
output.</p>

<h2>Task 3: AES Modes in Practice</h2>
<p>We used the PyCA <code>cryptography</code> library with a fresh random AES-256 key.
The message was <code>{html.escape(t3_msg)}</code> (45 characters / 45 bytes). CBC used a
fresh random 16-byte IV with PKCS7 padding. CTR used a fresh random 16-byte nonce/counter
block with no padding. The values below come from the saved run in Appendix A.2. The key,
IV and nonce are random, so the hex values differ on every run, but the lengths do not.</p>
<table>
<tr><th></th><th>AES-CBC</th><th>AES-CTR</th></tr>
<tr><td>IV / nonce (hex)</td><td class="hex">{t3_cbc_iv}</td><td class="hex">{t3_ctr_nonce}</td></tr>
<tr><td>Plaintext length</td><td>45 bytes</td><td>45 bytes</td></tr>
<tr><td>Ciphertext length</td><td>{t3_cbc_len}</td><td>{t3_ctr_len}</td></tr>
<tr><td>Ciphertext (hex)</td><td class="hex">{t3_cbc_ct}</td><td class="hex">{t3_ctr_ct}</td></tr>
<tr><td>Recovered plaintext matches exactly?</td><td>{t3_cbc_ok}</td><td>{t3_ctr_ok}</td></tr>
</table>
<p>The script compares each recovered plaintext with the original using <code>==</code>
and stops with an error if either does not match. Both passed.</p>

<h3>Observations comparing CBC and CTR</h3>
<ol>
<li><b>Padding and ciphertext length.</b> CBC works on whole 16-byte blocks, so the
45-byte message was PKCS7-padded to 48 bytes (3 blocks), and the ciphertext is longer than
the plaintext. CTR turns AES into a stream cipher: it XORs the plaintext with a keystream
made by encrypting the counter, so it needs no padding and the ciphertext is exactly 45
bytes. Neither mode hides the message length.</li>
<li><b>Parallelism.</b> CBC encryption is sequential, because each block is XORed with the
previous ciphertext block before encryption (CBC decryption can run in parallel). In CTR
every block uses its own counter value, so encryption and decryption can both run in
parallel, and any block can be decrypted on its own.</li>
<li><b>IV/nonce reuse.</b> Reusing a CTR nonce with the same key repeats the keystream,
so XORing two ciphertexts gives the XOR of the two plaintexts. This is catastrophic.
Reusing a CBC IV is also wrong but milder: it reveals when two messages begin with the
same blocks. Both modes here use a fresh random value on every encryption.</li>
<li><b>Error propagation and malleability.</b> Flipping one bit of a CBC ciphertext block
garbles that whole plaintext block and flips the same bit in the next block. In CTR it
flips exactly one plaintext bit, so an attacker can make precise changes without knowing
the key. Neither mode provides integrity, which motivates Task 4.</li>
</ol>

<h2>Task 4: Integrity and Tampering</h2>
<p>We computed a SHA-256 hash and an HMAC-SHA256 tag (with a fresh 32-byte random key) for
the original message, then changed one character, <code>fox</code> to <code>box</code>
(index 16, <code>f</code> to <code>b</code>), and recomputed both. Values are from the saved
run in Appendix A.3.</p>
<table>
<tr><th></th><th>Original message</th><th>Modified message</th></tr>
<tr><td>Message</td><td><code>The quick brown fox jumps over the lazy dog!!</code></td>
    <td><code>The quick brown box jumps over the lazy dog!!</code></td></tr>
<tr><td>SHA-256</td><td class="hex">{t4_sha_o}</td><td class="hex">{t4_sha_m}</td></tr>
<tr><td>HMAC-SHA256</td><td class="hex">{t4_tag_o}</td><td class="hex">{t4_tag_m}</td></tr>
<tr><td>HMAC verification against the original tag</td><td><b>PASS</b></td><td><b>FAIL</b></td></tr>
</table>

<p><b>How the digest/tag changed.</b> One changed character flipped
<b>{t4_sha_bits}</b> of the SHA-256 digest bits and <b>{t4_tag_bits}</b> of the HMAC tag
bits. The outputs look completely unrelated, which is the avalanche effect again, so no one
can tell from the outputs how similar the two messages were.</p>

<p><b>Verification.</b> The receiver, who holds the key, recomputes the tag and compares it
in constant time with <code>hmac.compare_digest</code>. The original message verifies
(<b>PASS</b>) and the modified message is rejected (<b>FAIL</b>).</p>

<p><b>Why a plain hash does not authenticate the sender.</b> SHA-256 uses no secret, so
anyone can compute it, including an attacker. If a sender transmits the message together
with its SHA-256 hash, an attacker in the middle can change the message, recompute the hash
and replace it. The receiver's check then passes and the forgery is accepted. Our run shows
this: the attacker's recomputed hash passed the receiver's check (<i>tampering NOT
detected</i>). A plain hash only detects accidental corruption.</p>

<p><b>Why HMAC provides integrity and authentication.</b> HMAC mixes a secret key into the
hash, so only someone who holds the key can produce a valid tag. An attacker without the
key cannot compute a matching tag for a changed message. In our run, the attacker's tag
failed verification (<i>tampering detected</i>). A valid tag therefore shows that the
message was not changed (<b>integrity</b>) and that it came from a holder of the shared key
(<b>authentication</b>). HMAC does not give non-repudiation, because both parties share
the key. That would need a digital signature.</p>

<h2>Task 5: Reflection</h2>
<p><b>The most important security lesson we learned:</b></p>
{REFLECTION}

<p><b>Video presentation:</b> {video_html}<br>
<span class="note">The video (5 minutes or less) includes all group members, shows each
program running, and explains the security meaning of the results.</span></p>

<h2 class="pagebreak">Appendix: Code and Program Output</h2>
<p class="note">To reproduce: <code>pip install -r requirements.txt</code>, then
run each script from the <code>block_ciphers_aes_and_des</code> folder.</p>

<h3>A.1 Task 2: <code>task2_avalanche/avalanche.py</code></h3>
{pre("task2_avalanche/avalanche.py")}
<p><b>Output</b> (<code>results/task2_avalanche_output.txt</code>):</p>
<pre class="out">{html.escape(read("results/task2_avalanche_output.txt").rstrip())}</pre>

<h3>A.2 Task 3: <code>task3_aes_modes/aes_modes.py</code></h3>
{pre("task3_aes_modes/aes_modes.py")}
<p><b>Output</b> (<code>results/task3_aes_modes_output.txt</code>):</p>
<pre class="out">{html.escape(t3.rstrip())}</pre>

<h3>A.3 Task 4: <code>task4_integrity/integrity.py</code></h3>
{pre("task4_integrity/integrity.py")}
<p><b>Output</b> (<code>results/task4_integrity_output.txt</code>):</p>
<pre class="out">{html.escape(t4.rstrip())}</pre>

</body>
</html>
"""

# Task 5 on its own: group details, reflection and video link
head = page.split("<body>")[0]
refl_page = f"""{head.replace("Group Report", "Task 5 Reflection")}<body>
<div class="cover">
<h1>Task 5: Reflection and Video Presentation</h1>
<p class="sub"><b>CSC 3114: Cryptology and Coding Theory</b>, Take-Home Assignment (Test 2)</p>
<p class="sub">Block Ciphers, AES and Integrity</p>
<h2>Group Members: {GROUP}</h2>
<table>
<tr><th>#</th><th>Name</th><th>Registration No.</th><th>Student No.</th><th>Tasks</th></tr>
{members_rows}
</table>
</div>
<h2>Reflection: The Most Important Security Lesson</h2>
{REFLECTION}
<h2>Video Presentation</h2>
<p><b>Link:</b> {video_html}</p>
<p>The video (5 minutes or less):</p>
<ul>
<li>includes all group members;</li>
<li>shows evidence that the code runs (Tasks 2, 3 and 4 executed live);</li>
<li>explains the security meaning of the results rather than reading code line by line;</li>
<li>is uploaded to Google Drive, accessible to the lecturer through the link above.</li>
</ul>
</body>
</html>
"""

browser = find_browser()
for html_path, pdf_path, content in [
    (OUT_HTML, OUT_PDF, page),
    (REFL_HTML, REFL_PDF, refl_page),
]:
    html_path.write_text(content, encoding="utf-8")
    print(f"Wrote {html_path}")
    if browser is None:
        print(f"No Edge/Chrome found: open {html_path.name} in a browser and Print > Save as PDF.")
        continue
    subprocess.run(
        [browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf_path}", html_path.as_uri()],
        check=True, capture_output=True,
    )
    print(f"Wrote {pdf_path}")

missing = [m for m in MEMBERS for v in m[:3] if v.startswith("[")] or VIDEO_LINK.startswith("[")
if missing:
    print("NOTE: names, registration numbers or the video link are still placeholders.")
