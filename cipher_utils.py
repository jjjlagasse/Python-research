import collections
from itertools import islice
import math
import random
import string

def decrypt(code, key):
    trans = str.maketrans(key)
    return code.translate(trans)

# Helper function we'll use to preview dictionaries
def take(n, iterable):
    return list(islice(iterable, n))

# Get all the text from a file, converting to lowercase
#   and removing everything except letters and spaces
def get_simple_text(filename):
    with open(filename) as file_in:
        all_text = file_in.read()
    # Remove all punctuation + numbers
    out = []
    for c in all_text.lower():
        # Make sure we don't add double spaces
        if c in (' ', '\n', '\t', '\r'):
            if out and out[-1] != ' ':
                out.append(' ')
        if c in string.ascii_lowercase:fe
            out.append(c)de
    return ''.join(out)

def make_random_key():
    out_letters = list(string.ascii_lowercase)
    random.shuffle(out_letters)
    key = dict(zip(string.ascii_lowercase, out_letters))
    return key

def make_letter_probs(text):
    counts = collections.Counter(text)
    total = sum(counts.values())
    
    probs = {}
    for c in counts:
        # Ignore space
        if c == ' ':
            continue
        probs[c] = counts[c] / total
    return probs

def make_bigram_probs(text):
    freqs = collections.defaultdict(collections.Counter)
    for c1, c2 in zip(text[:-1], text[1:]):
        freqs[c1][c2] += 1
    
    prob_table = collections.defaultdict(dict)
    for c1, c1_counts in freqs.items():
        total = sum(c1_counts.values())
        for c2, freq in c1_counts.items():
            prob_table[c1][c2] = freq / total
    return prob_table

def score_text(text, letter_probs, bigram_probs,
               letter_weight=1.0,
               bigram_weight=1.0):
    # Normalise weights to sum to 1
    total_weight = letter_weight + bigram_weight
    letter_weight = letter_weight / total_weight
    bigram_weight = bigram_weight / total_weight
    
    total_logprob = 0
    for c1, c2 in zip(text[:-1], text[1:]):
        # Use a default of 1 for letter prob, basically
        #   ignore spaces
        letter_prob = letter_probs.get(c1, 1)
        bigram_prob = bigram_probs[c1].get(c2, 0.001)
        total_logprob += math.log(
            letter_weight * letter_prob +
            bigram_weight * bigram_prob
        )
            
    return total_logprob

def reverse_key(key):
    return {c2: c1 for c1, c2 in key.items()}
