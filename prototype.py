import random
import csv

cards = []
with open('db.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",")
    for row in spamreader:
        cards.append(row)

def guess():
    i = random.randint(0,51)
    print(cards[i][0])
    input()
    print(cards[i][1])

while True:
    n = input('wanna try?')
    if n == 'y':
        guess()
    else:
        break