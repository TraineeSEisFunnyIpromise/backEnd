from collections import Counter
import nltk
from nltk.tokenize import word_tokenize

# Sample description
description = "Step-by-step instructions for baking a delicious chocolate cake. This chocolate cake recipe is perfect for any occasion."

# Tokenize the description into individual words
tokens = word_tokenize(description)

# Count the frequency of each word
word_counts = Counter(tokens)

# Print the word frequencies
for word, count in word_counts.items():
    print(f"'{word}': {count}")