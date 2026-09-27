import sqlite3
import re

DB = "markov.db"

token_re = re.compile(r"\b\w+[.!?]?")

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS transitions (
    w1 TEXT,
    w2 TEXT,
    w3 TEXT,
    cnt INTEGER,
    PRIMARY KEY (w1, w2, w3)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS sentence_starts (
    w1 TEXT,
    w2 TEXT
)
""")

conn.commit()

print("Training gestartet...")

with open("RC_2019-01.txt", encoding="utf8", errors="ignore") as f:
    for i, line in enumerate(f):
        line = line.strip().lower()
        if not line:
            continue

        words = token_re.findall(line)
        if len(words) < 3:
            continue

        # Satzanfang
        cur.execute(
            "INSERT INTO sentence_starts VALUES (?, ?)",
            (words[0], words[1])
        )

        for j in range(len(words) - 2):
            w1, w2, w3 = words[j], words[j+1], words[j+2]
            cur.execute("""
            INSERT INTO transitions VALUES (?, ?, ?, 1)
            ON CONFLICT(w1, w2, w3)
            DO UPDATE SET cnt = cnt + 1
            """, (w1, w2, w3))

        if i % 10000 == 0:
            conn.commit()
            print(f"{i} Zeilen verarbeitet")

conn.commit()
conn.close()
print("Training fertig.")
