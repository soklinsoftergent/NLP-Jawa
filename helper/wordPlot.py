import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 1. Load your data (Assuming it's a CSV with 'Word' and 'Frequency')
df = pd.read_csv('javanese_word_frequency1.csv') 
# For this demo, I'll use your top words:
# data = {
#     'Word': ['ing', 'kang', 'ingkang', 'wong', 'lan', 'sang', 'punika', 'sampun', 'yèn', 'wontên', 'para', 'wus', 'tan', 'sami'],
#     'Frequency': [510249, 291619, 253248, 134747, 128840, 126354, 120227, 103499, 87043, 85283, 83258, 83149, 82314, 81088]
# }
# df = pd.DataFrame(data)

# Convert to a dictionary for the word cloud
word_freq = dict(zip(df['Word'], df['Frequency']))

# Create the Word Cloud
wc = WordCloud(width=1000, height=600, 
               background_color='white', 
               colormap='copper', # Gives it a royal/golden look
               max_words=100).generate_from_frequencies(word_freq)

plt.figure(figsize=(15, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('Top Concepts in the Javanese Diachronic Corpus', fontsize=20)
plt.show()

import numpy as np

# Sort by frequency descending and create a 'Rank' column
df = df.sort_values('Frequency', ascending=False)
df['Rank'] = np.arange(1, len(df) + 1)

plt.figure(figsize=(10, 6))
plt.loglog(df['Rank'], df['Frequency'], marker=".", linestyle='none', alpha=0.5)
plt.xlabel('Rank (log scale)')
plt.ylabel('Frequency (log scale)')
plt.title('Zipf\'s Law Analysis: Javanese Corpus Stability')
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.show()

import seaborn as sns

# Calculate length of each word
df['Length'] = df['Word'].apply(lambda x: len(str(x)))

plt.figure(figsize=(12, 6))
sns.histplot(df['Length'], bins=range(1, 25), kde=True, color='brown')
plt.title('How long are Javanese words in your corpus?')
plt.xlabel('Number of Characters')
plt.ylabel('Number of Unique Words')
plt.show()

