from os import system
from random import randint
from time import sleep
tails = 0
heads = 0
while True:
    system('clear')
    print('Total number of flips: %d\nTotal number of Heads: %d\nTotal number of Tails: %d' %(heads + tails, heads, tails))
    s = input('Press "enter" to flip the coin or "exit" to quit the experiment\n')
    if s == 'exit':
        break
    elif len(s) == 0:
        result = randint(0, 2)
        if result == 0:
            heads += 1
            print("It's a Head")
        else:
            tails += 1
            print("It's a Tail")
        sleep(0.5)
system('clear')
print('## RESULTS ##')
print('Total number of flips: %d\nTotal number of Heads: %d\nTotal number of Tails: %d' %(heads + tails, heads, tails))

