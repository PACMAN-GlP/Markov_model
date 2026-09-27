import random
import pickle

with open("markov_model2.pkl", "rb") as f:
    model, sentence_starts = pickle.load(f)

def generate(seed=None, max_words=50):
    # Start: entweder User-Seed oder zufälliger Satzanfang
    if seed:
        words = seed.lower().split()
        if len(words) >= 2:
            w1, w2 = words[-2], words[-1]
        else:
            w1, w2 = random.choice(sentence_starts)
    else:
        w1, w2 = random.choice(sentence_starts)

    output = [w1, w2]

    for _ in range(max_words):
        next_words = model.get((w1, w2))
        if not next_words:
            break

        w3 = random.choice(next_words)
        output.append(w3)

        # Sauber beenden
        if w3.endswith((".", "!", "?")):
            break

        w1, w2 = w2, w3

    return " ".join(output)

print("Bot bereit. 'exit' zum Beenden.\n")

while True:
    user = input("You: ").strip()
    if user.lower() == "exit":
        break

    response = generate(user)
    print("Reddit:", response)
