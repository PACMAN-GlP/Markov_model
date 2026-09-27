from collections import defaultdict
import pickle

model = defaultdict(list)
sentence_starts = []

print("Training gestartet...")

with open("RC_2019-01_clean.txt", encoding="utf8") as f:
    for i, line in enumerate(f):
        line = line.strip().lower()
        if not line:
            continue

        words = line.split()
        if len(words) < 3:
            continue

        # Satzanfang merken
        if words[0][0].isalpha():
            sentence_starts.append((words[0], words[1]))

        # N-Gram lernen
        for j in range(len(words) - 2):
            w1 = words[j]
            w2 = words[j + 1]
            w3 = words[j + 2]
            model[(w1, w2)].append(w3)

        if i % 100000 == 0 and i > 0:
            print(f"{i} Zeilen verarbeitet")

print("Training fertig.")
print("Modellgröße:", len(model))
print("Sentence starts:", len(sentence_starts))

# Modell speichern
with open("model3.pkl", "wb") as f:
    pickle.dump((model, sentence_starts), f)

print("Gespeichert unter model3.pkl")
