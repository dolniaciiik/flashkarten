from flask import Flask, render_template, request, redirect, url_for
import random
import csv
import os

app = Flask(__name__)

SET_DIR = "sets"

# Load cards from a given set
def load_cards(set_filename):
    path = os.path.join(SET_DIR, set_filename)
    if not os.path.isfile(path):
        return []
    
    cards = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) >= 2:
                cards.append(row)
    return cards

# Memory (per session run)
used_indices = {}
sequential_indices = {}
loaded_sets = {}

def gen_cardnum_random(set_name, total):
    if set_name not in used_indices:
        used_indices[set_name] = set()

    used = used_indices[set_name]

    if len(used) >= total:
        used.clear()

    i = random.randint(0, total - 1)
    while i in used:
        i = random.randint(0, total - 1)

    used.add(i)
    return i

def gen_cardnum_sequential(set_name, total):
    if set_name not in sequential_indices:
        sequential_indices[set_name] = 0
    idx = sequential_indices[set_name]
    sequential_indices[set_name] = (idx + 1) % total
    return idx

@app.route("/")
def index():
    set_files = [f for f in os.listdir(SET_DIR) if f.endswith(".csv")]
    
    set_cards = {}
    for fname in set_files:
        path = os.path.join(SET_DIR, fname)
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            set_cards[fname] = [row for row in reader if len(row) >= 2]

    return render_template("index.html", sets=set_files, set_cards=set_cards)
@app.route("/cards/")
def card():
    set_name = request.args.get("set")
    mode = request.args.get("mode", "random")  # default is random

    if not set_name:
        return redirect(url_for("index"))

    if set_name not in loaded_sets:
        cards = load_cards(set_name)
        loaded_sets[set_name] = cards
    else:
        cards = loaded_sets[set_name]

    if not cards:
        return f"<h1 style='color:white;background:#121212;padding:2rem;'>No cards found in {set_name}</h1>"

    if mode == "sequential":
        idx = gen_cardnum_sequential(set_name, len(cards))
    else:
        idx = gen_cardnum_random(set_name, len(cards))

    question, answer = cards[idx]
    return render_template("card.html", question=question, answer=answer, set_name=set_name, mode=mode)
