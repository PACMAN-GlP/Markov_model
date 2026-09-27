import sqlite3
import random

conn = sqlite3.connect("markov.db")
cur = conn.cursor()

def random_start():
    cur.execute("""
        SELECT w1, w2 FROM sentence_starts
        ORDER BY RANDOM() LIMIT 1
    """)
    return cur.fetchone()

def next_word(w1, w2):
    cur.execute("""
        SELECT w3, cnt FROM transitions
        WHERE w1=? AND w2=?
    """, (w1, w2))

    rows = cur.fetchall()
    if not rows:
        return None

    words, weights = zip(*rows)
    return random.choices(words, weights=weights, k=1)[0]

def generate(seed=None, max_words=50):
    if seed:
        parts = seed.lower().split()
        if len(parts) >= 2:
            w1, w2 = parts[-2], parts[-1]
        else:
            w1, w2 = random_start()
    else:
        w1, w2 = random_start()

    output = [w1, w2]

    for _ in range(max_words):
        w3 = next_word(w1, w2)
        if not w3:
            break
        output.append(w3)
        if w3.endswith((".", "!", "?")):
            break
        w1, w2 = w2, w3

    return " ".join(output)

print("Bot bereit. 'exit' zum Beenden.\n")

while True:
    user = input("You: ").strip()
    if user.lower() == "exit":
        break
    print("Reddit:", generate(user))
