# Read the cleaned text
with open("cleans/javanese_clean.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Simple tokenization (split by whitespace)
tokens = text.split()

print(tokens[:50])  # See first 50 tokens
print("Total tokens:", len(tokens))

from collections import Counter

# Count word frequencies
word_freq = Counter(tokens)

# Print 20 most common words
for word, freq in word_freq.most_common(20):
    print(word, freq)

# Save to CSV
import csv
with open("javanese_word_frequency1.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Word", "Frequency"])
    for word, freq in word_freq.most_common():
        writer.writerow([word, freq])

print("Word frequencies saved to javanese_word_frequency.csv")

