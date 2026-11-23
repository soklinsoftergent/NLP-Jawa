# smart_remove_english.py
import re
import csv
from collections import Counter
import sys

# ---------- Settings (tweak these) ----------
CORPUS_IN = r"javanese_clean.txt"            # your cleaned text file (multiline)
CORPUS_OUT = r"javanese_no_english.txt"      # output file
REPORT_CSV = r"removed_candidates_report.csv"  # report: tokens considered for removal

# frequency threshold: tokens with freq >= this are assumed Javanese (keep)
KEEP_FREQ_THRESHOLD = 200           # keep tokens that appear >= this many times
# rare threshold: tokens with freq <= this AND likely-English -> remove
RARE_FREQ_THRESHOLD = 50            # candidate for removal if <= this

# Minimum token length to consider (short tokens like 'a' or 'i' rarely informative)
MIN_KEEP_LEN = 2

# Optional manual whitelist of known Javanese function words you NEVER want removed
JAVANESE_WHITELIST = {
    "ing","lan","lan","kang","iku","iki","saka","kanggo","punika",
    "uga","utawa","ana","dadi","karo","minangka","ingkang","iku","iki",
    "saking","wonten","basa","kuwi","kuwi","kayata","amarga","nalika","sawijining"
}

# small Indonesian blacklist to remove (domain words)
INDONESIAN_STOPWORDS = {
    "yang","dan","di","ke","pada","dari","adalah","itu","untuk","dengan","sebagai",
    "dalam","juga","atau","ini","karena","oleh","sudah","tidak","akan","mereka",
    "kami","saya","kamu","berita","provinsi","kabupaten","kecamatan","desa","taun",
}

# load NLTK english words if available, otherwise load minimal english set
try:
    import nltk
    nltk.data.find("corpora/words")
    from nltk.corpus import words as nltk_words
    ENGLISH_WORDS = set(w.lower() for w in nltk_words.words())
except Exception:
    # minimal high-frequency english words (expand as wanted)
    ENGLISH_WORDS = set([
        "the","and","is","in","of","to","for","on","with","this","that","are","was","it",
        "from","as","by","be","an","at","or","but","about","not","we","can","you","they",
        "have","has","will","if","when","then","there","which","he","she","his","her","name",
        "type","population","subdivision","blank"
    ])

# regex for tokenization (keep Latin letters + Javanese script)
TOKEN_RE = re.compile(r"[A-Za-z\uA980-\uA9DF]+", flags=re.UNICODE)

# ---------- Step 1: build token frequency ----------
print("Counting tokens...")
counter = Counter()
with open(CORPUS_IN, "r", encoding="utf-8") as f:
    for line in f:
        for tok in TOKEN_RE.findall(line):
            tok_l = tok.lower()
            counter[tok_l] += 1

print("Total unique tokens:", len(counter))
print("Total tokens (rough):", sum(counter.values()))

# ---------- Step 2: build keep set by frequency and script presence ----------
keep_set = set()
# Keep everything that contains Javanese script characters (unicode A980-A9DF)
jav_script_re = re.compile(r"[\uA980-\uA9DF]")
for token, freq in counter.items():
    if freq >= KEEP_FREQ_THRESHOLD:
        keep_set.add(token)
    elif jav_script_re.search(token):
        # preserve any token using Javanese script (if present)
        keep_set.add(token)
    elif token in JAVANESE_WHITELIST:
        keep_set.add(token)

print("Pre-marked keep tokens (by freq/script/whitelist):", len(keep_set))

# ---------- Step 3: candidate removal decision ----------
removed_candidates = []   # (token, freq, reason)
final_keep = set(keep_set)  # tokens to definitely keep

for token, freq in counter.items():
    if token in final_keep:
        continue
    # length guard: keep short tokens if in whitelist
    if len(token) < MIN_KEEP_LEN:
        final_keep.add(token)
        continue

    lowered = token.lower()
    # if token clearly Indonesian stopword, mark for removal
    if lowered in INDONESIAN_STOPWORDS:
        removed_candidates.append((token, freq, "indonesian_stopword"))
        continue

    # if token is English word and it's rare in the corpus -> remove
    if lowered in ENGLISH_WORDS and freq <= RARE_FREQ_THRESHOLD:
        removed_candidates.append((token, freq, "english_rare"))
        continue

    # If token contains typical metadata patterns (px, iso, en-us etc) or digits, remove
    if re.search(r"\d", token) or token.endswith("px") or re.match(r"^[a-z]{1,3}$", token) and lowered in {"px","iso","utc"}:
        removed_candidates.append((token, freq, "technical"))
        continue

    # otherwise keep it
    final_keep.add(token)

print("Candidates marked for removal:", len(removed_candidates))

# ---------- Step 4: write cleaned corpus streaming (preserve newlines) ----------
print("Writing filtered corpus...")
with open(CORPUS_IN, "r", encoding="utf-8") as fin, open(CORPUS_OUT, "w", encoding="utf-8") as fout:
    for line in fin:
        tokens_out = []
        for tok in TOKEN_RE.findall(line):
            t = tok.lower()
            if t in final_keep:
                tokens_out.append(tok)    # preserve original case/form
            # else skip it (removed)
        if tokens_out:
            fout.write(" ".join(tokens_out) + "\n")

# ---------- Step 5: save removal report ----------
with open(REPORT_CSV, "w", encoding="utf-8", newline="") as csvf:
    writer = csv.writer(csvf)
    writer.writerow(["token","frequency","reason"])
    # sort by freq desc for inspection
    for tok,freq,reason in sorted(removed_candidates, key=lambda x: -x[1]):
        writer.writerow([tok,freq,reason])

print("Done.")
print("Filtered corpus:", CORPUS_OUT)
print("Removal candidates report:", REPORT_CSV)
print("Notes: tweak KEEP_FREQ_THRESHOLD and RARE_FREQ_THRESHOLD if too aggressive / lax.")
