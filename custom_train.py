import re

print("Initializing...")

pattern = re.compile(r"^[a-zA-Z0-9.,!?']+$")
repeat_pattern = re.compile(r"(.)\1{3,}")
begin_pattern = re.compile(r"^[a-zA-Z']")
camel_case_pattern = re.compile(r"[A-Z][a-z]*[A-Z]")

word_counts = {}
words_written = 0
words_read=0
frequent_word=""
frequent_word_count=0

def is_valid_word(word):
    return bool(pattern.match(word))

def has_repeated_chars(word):
    return bool(repeat_pattern.search(word))

def is_valid_start(word):
    return bool(begin_pattern.match(word))

def is_combined_word(word):
    return bool(camel_case_pattern.search(word))

def valid_punctuation(word):
    for char in ".!?,":
        if word.count(char) > 1:
            return False

    for char in "\"'":
        if word.count(char) > 2:
            return False

    return True


print("reading model...")
try:
    with open("Reddit_model.txt", "r", encoding="utf-8") as g:
        for line in g:
            parts = line.strip().split()
            if len(parts) == 2:
                word, count = parts
                word_counts[word] = int(count)
except FileNotFoundError:
    print("File Reddit_model.txt not found")

print("reading data...")
with open("sample_500mb.txt", "r", encoding="utf-8") as f:
    for line in f:
        for word in line.strip().split():
            words_read += 1
            if not is_valid_word(word) or has_repeated_chars(word) or not is_valid_start(word) or not is_combined_word(word) or not valid_punctuation(word):
                continue
            word_counts[word] = word_counts.get(word, 0) + 1
print(f"{words_read} words read.")

print("completing model...")
with open("Reddit_model.txt", "w", encoding="utf-8") as g:
    for word, count in sorted(word_counts.items()):
        g.write(f"{word} {count}\n")
        words_written += 1
        if count > frequent_word_count:
            frequent_word_count += count
            frequent_word = word
print(f"{words_written} words written.")

print(f"most frequent word: {frequent_word} - {frequent_word_count}")
