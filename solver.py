from collections import defaultdict, Counter
import itertools
import random

import requests
import re
import argparse

WORDED_INDEX = ["first", "second", "third", "fourth", "fifth", "sixth"]

LETTER_FREQUENCY = {
    'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31,
    'n': 6.95, 's': 6.28, 'h': 5.92, 'r': 6.02, 'd': 4.32,
    'l': 3.98, 'u': 2.88, 'c': 2.71, 'm': 2.61, 'f': 2.30,
    'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
    'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.10,
    'z': 0.07
}

WORD_LENGTH = 5 
ATTEMPTS_COUNT = 6
FORBIDDEN_FEATURE_ACTIVE = False
SUGGESTIONS_COUNT = 20

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Wordle Solver")
    parser.add_argument("--word-length", type=int, default=WORD_LENGTH,
                        help="Length of the words to guess (default: 5)")
    parser.add_argument("--attempts", type=int, default=ATTEMPTS_COUNT,
                        help="Number of attempts allowed (default: 6)")
    parser.add_argument("--disable-fetch", action='store_true',
                        help="Disable fetching word list from online source")
    parser.add_argument("--suggestions-count", type=int, default=SUGGESTIONS_COUNT,
                        help="Number of suggestions to show at once (default: 20)")
    return parser.parse_args()

args = parse_args()
WORD_LENGTH = args.word_length
ATTEMPTS_COUNT = args.attempts
FORBIDDEN_FEATURE_ACTIVE = not args.disable_fetch
SUGGESTIONS_COUNT = args.suggestions_count

def fetch_word_list():
    """Fetch a list of valid words from an online source."""
    if not FORBIDDEN_FEATURE_ACTIVE:
        print("Word list fetching is disabled.")
        return []
    
    print("Fetching word list from Meaningpedia...")
    meaningpedia_resp = requests.get(f"https://meaningpedia.com/{WORD_LENGTH}-letter-words?show=all")
    if meaningpedia_resp.status_code != 200:
        print("Failed to fetch word list.")
        return []
    
    pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
    world_list = pattern.findall(meaningpedia_resp.text)
    return {word.lower() for word in world_list if len(word) == WORD_LENGTH}

word_list = fetch_word_list()
if not word_list:
    print("No valid words found. Using random letter combinations instead.")

weights = [[] for _ in range(WORD_LENGTH)]
green_letters = [None] * WORD_LENGTH
yellow_letters = defaultdict(list)
gray_letters = set()
words = []

def process_letters(word, yletters, gletters):
    """Process user input and update letter tracking."""
    global gray_letters

    word = word.lower()
    word_counter = Counter(word)
    y_counter = Counter(yletters)
    g_counter = Counter(gletters)

    for letter in word_counter:
        total_uses = y_counter[letter] + g_counter[letter]
        if total_uses < word_counter[letter]:
            gray_letters.add(letter)

    for i, letter in enumerate(word):
        if g_counter[letter] > 0:
            green_letters[i] = letter
            weights[i] = [letter] * WORD_LENGTH
            g_counter[letter] -= 1

    for i, letter in enumerate(word):
        if y_counter[letter] > 0 and green_letters[i] != letter:
            yellow_letters[i].append(letter)
            weights[i].append(letter)
            y_counter[letter] -= 1

def suggest_words():
    """Generate 10-20 valid variable sized words with green letters fixed in place."""
    suggestions = set()

    # Set of all letters that must appear in the word
    mandatory_letters = set(filter(None, green_letters))
    for lst in yellow_letters.values():
        mandatory_letters.update(lst)

    allowed_letters = [l for l in LETTER_FREQUENCY if l not in gray_letters]
    allowed_letters.sort(key=lambda l: -LETTER_FREQUENCY[l])

    # Generate candidate letter sets
    for combo in itertools.permutations(allowed_letters, WORD_LENGTH):
        candidate = list(combo)

        green_mismatch = any(
            green_letters[i] and candidate[i] != green_letters[i]
            for i in range(WORD_LENGTH)
        )
        if green_mismatch:
            continue

        if not mandatory_letters.issubset(candidate):
            continue

        yellow_misplaced = any(
            candidate[i] in yellow_letters[i]
            for i in range(WORD_LENGTH)
        )
        if yellow_misplaced:
            continue
        suggestions.add("".join(candidate))
    
    good_suggestions = [w for w in suggestions if w in word_list] if word_list else list(suggestions)
    good_suggestions.sort(key=lambda w: -sum(LETTER_FREQUENCY[c] for c in set(w)))

    suggestions_list = list(suggestions)
    for s in range(20 - len(good_suggestions)):
        if suggestions_list:
            good_suggestions.append(suggestions_list[random.randint(0, len(suggestions_list) - 1)])
    return good_suggestions

def show_interface():
    print("------------- Wordle Solver -------------\n")

    for i in range(ATTEMPTS_COUNT):
        print(f"Round {i + 1}")
        while True:
            word = input(f"Enter the {WORDED_INDEX[i]} guessed word (5 letters): ").lower().strip()
            if len(word) == WORD_LENGTH and word.isalpha():
                break
            print(f"Invalid input. Please enter a {WORD_LENGTH}-letter word.")
        yletters = list(input("Enter yellow letters (repeat if needed): ").lower().strip())
        gletters = list(input("Enter green letters: ").lower().strip())

        words.append(word)
        process_letters(word, yletters, gletters)

        print("\nCalculating suggestions...")
        suggestions = suggest_words()

        index_offset = 0
        while input(f"Do you want to see {"the" if index_offset == 0 else "more"} suggestions? (y/N): ").lower().strip() == 'y':
            print("\nSuggestions:")
            for s in suggestions[index_offset:index_offset + SUGGESTIONS_COUNT]:
                print(f"  - {s}")
            index_offset += SUGGESTIONS_COUNT

        print("\n" + "-" * 30 + "\n")

if __name__ == "__main__":
    show_interface()

