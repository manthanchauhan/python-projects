import pandas as pd
import random
import time
import tkinter
from string import Template
from tkinter.constants import Y, YES


def probability(stat):
    pokemon_c = deck_c[0]
    greater = 0
    lesser = 0
    equal = 0
    if stat == 'hp':
        i = 1
    elif stat == 'attack':
        i = 2
    else:
        i = 3
    for pokemon_p in deck_p:
        if cards[pokemon_c][i] > cards[pokemon_p][i]:
            lesser += 1
        elif cards[pokemon_p][i] > cards[pokemon_c][i]:
            greater += 1
        else:
            equal += 1
    return lesser / (lesser + greater + equal)


def proceed():
    global update
    update = True
    global chance
    text.delete(0.1, 4.20)
    show_card('player')
    show_card('random')
    if chance == 'player':
        text.insert(0.1, 'Make your move')
    else:
        prob_hp = probability('hp')
        prob_atk = probability('attack')
        prob_def = probability('defense')
        if prob_hp >= prob_atk and prob_hp >= prob_def:
            make_move(False, 1)
        elif prob_atk >= prob_hp and prob_atk >= prob_def:
            make_move(False, 2)
        else:
            make_move(False, 3)


def show_card(s):
    if s == 'player':
        pokemon = deck_p[0]
        name_p.set('Name: ' + pokemon)
        type_p.set('Type: ' + cards[pokemon][0])
        hp_p.set('HP: ' + str(cards[pokemon][1]))
        attack_p.set('Attack: ' + str(cards[pokemon][2]))
        defense_p.set('Defense: ' + str(cards[pokemon][3]))
    elif s == 'computer':
        pokemon = deck_c[0]
        name_c.set('Name: ' + pokemon)
        type_c.set('Type: ' + cards[pokemon][0])
        hp_c.set('HP: ' + str(cards[pokemon][1]))
        attack_c.set('Attack: ' + str(cards[pokemon][2]))
        defense_c.set('Defense: ' + str(cards[pokemon][3]))
    else:
        name_c.set('Name: ')
        type_c.set('Type: ')
        hp_c.set('HP: ')
        attack_c.set('Attack: ')
        defense_c.set('Defense: ')


def make_move(player, move):
    text.delete(1.0, 4.20)
    global update
    if not update:
        text.insert(1.0, 'Press button ---->')
        return
    global chance
    if chance == 'computer' and player:
        text.insert(0.1, "Hey,\nit's not your turn")
        return
    show_card('computer')
    pokemon_p = deck_p[0]
    pokemon_c = deck_c[0]
    if player and move == 1:
        message = 'You chose HP: ' + str(cards[pokemon_p][1]) + "\nComputer's HP: " + str(cards[pokemon_c][1]) + \
                  '\nThis was a ${decision} battle'
    elif player and move == 2:
        message = 'You chose Attack: ' + str(cards[pokemon_p][2]) + "\nComputer's Attack: " + str(cards[pokemon_c][2])\
                  + '\nThis was a ${decision} battle'
    elif player and move == 3:
        message = 'You chose Defense: ' + str(cards[pokemon_p][3]) + "\nComputer's Defense: " + str(cards[pokemon_c][3])\
                  + '\nThis was a ${decision} battle'
    elif (not player) and move == 1:
        message = 'Computer chose HP: ' + str(cards[pokemon_c][1]) + "\nYour HP: " + str(cards[pokemon_p][1]) + \
                  '\nThis was a ${decision} battle'
    elif (not player) and move == 2:
        message = 'Computer chose Attack: ' + str(cards[pokemon_c][2]) + "\nYour Attack: " + str(cards[pokemon_p][2]) +\
                  '\nThis was a ${decision} battle'
    else:
        message = 'Computer chose Defense: ' + str(cards[pokemon_c][3]) + "\nYour Defense: " + str(cards[pokemon_p][3])\
                  + '\nThis was a ${decision} battle'
    message = Template(message)
    if cards[pokemon_p][move] > cards[pokemon_c][move]:
        message = message.substitute(decision='winning')
        deck_p.append(deck_c[0])
        deck_p.append(deck_p[0])
        deck_c.pop(0)
        deck_p.pop(0)
        chance = 'player'
    elif cards[pokemon_p][move] == cards[pokemon_c][move]:
        message = message.substitute(decision='draw')
        deck_c.append(deck_c[0])
        deck_c.pop(0)
        deck_p.append(deck_p[0])
        deck_p.pop(0)
    else:
        message = message.substitute(decision='loosing')
        deck_c.append(deck_p[0])
        deck_p.pop(0)
        deck_c.append(deck_c[0])
        deck_c.pop(0)
        chance = 'computer'
    if len(deck_p) == 0:
        text.insert(0.1, 'You lost')
        time.sleep(3)
        tkinter.quit()
    elif len(deck_c) == 0:
        text.insert(0.1, 'You won')
        time.sleep(3)
        tkinter.quit()
    else:
        text.insert(0.1, str(message))
    update = False
    cards_left_p.set('Cards left: ' + str(len(deck_p)))
    cards_left_c.set('Cards left: ' + str(len(deck_c)))


# graphics..............................................................................................................
main_window = tkinter.Tk()
main_window1 = tkinter.Frame(main_window, bg='black', bd=5)
main_window1.pack(side='top', expand=YES, fill=Y)
main_window2 = tkinter.Frame(main_window)
main_window2.pack(side='bottom')
# main_window1
proceed_button = tkinter.Button(main_window1, bg='maroon2', font=('Arial', 14, 'bold'), height=3, width=7,
                                text='Proceed', command=proceed)
proceed_button.pack(side='right', fill=Y, expand=YES)
text = tkinter.Text(main_window1, bg='PeachPuff2', font=('Arial', 14, 'bold'), width=36, height=3)
text.insert(1.0, 'Hi!!!, Welcome in "POKEMON GO".\n')
text.insert(2.0, 'Choose one of the three stats to fight battles.')
text.pack(side='left', fill=Y, expand=YES)
# main_window2
player_arena = tkinter.Frame(main_window2, bd=10, bg='OliveDrab1')
player_arena.pack(side='left')
computer_arena = tkinter.Frame(main_window2, bd=10, bg='yellow2')
computer_arena.pack(side='right')
arena_name = tkinter.Label(player_arena, bg='OliveDrab1', font=('Arial', 14, 'bold'), width=19, height=1,
                           text="Player's Arena")
arena_name.pack(side='top')
arena_name = tkinter.Label(computer_arena, bg='yellow2', font=('Arial', 14, 'bold'), width=19, height=1,
                           text="Computer's Arena")
arena_name.pack(side='top')
cards_left_p = tkinter.StringVar()
cards_left_c = tkinter.StringVar()
cards_label_c = tkinter.Label(computer_arena, font=('Arial', 14, 'bold'), width=19, height=1, textvariable=cards_left_c,
                              anchor='w')
cards_label_c.pack(side='top')
cards_label_p = tkinter.Label(player_arena, font=('Arial', 14, 'bold'), width=19, height=1, textvariable=cards_left_p,
                              anchor='w')
cards_label_p.pack(side='top')
card_c = tkinter.Frame(computer_arena, bd=4, bg='cornflower blue')
card_c.pack(side='top')
card_p = tkinter.Frame(player_arena, bd=4, bg='purple1')
card_p.pack(side='top')
pokeball = tkinter.PhotoImage(file='D:\Git\python-projects\Pokemon game\pokeball.png')
# player's card
image_p = tkinter.Label(card_p, image=pokeball, width=217)
image_p.pack(side='top')
stats_p = tkinter.Frame(card_p)
name_p = tkinter.StringVar()
name_label_p = tkinter.Label(stats_p, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                             textvariable=name_p)
name_label_p.pack(side='top')
type_p = tkinter.StringVar()
type_label_p = tkinter.Label(stats_p, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                             textvariable=type_p)
type_label_p.pack(side='top')
hp_p = tkinter.StringVar()
attack_p = tkinter.StringVar()
defense_p = tkinter.StringVar()
hp_label_p = tkinter.Label(stats_p, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                           textvariable=hp_p)
hp_label_p.pack(side='top')
attack_label_p = tkinter.Label(stats_p, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                               textvariable=attack_p)
attack_label_p.pack(side='top')
defense_label_p = tkinter.Label(stats_p, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                                textvariable=defense_p)
defense_label_p.pack(side='top')
stats_p.pack(side='top')
moves_p = tkinter.Frame(card_p)
hp_button_p = tkinter.Button(moves_p, bg='deep sky blue', font=('Arial', 14, 'bold'), height=1, width=18, text='HP',
                             command=lambda: make_move(True, 1))
hp_button_p.pack(side='top')
attack_button_p = tkinter.Button(moves_p, bg='red2', font=('Arial', 14, 'bold'), height=1, width=18, text='ATK',
                                 command=lambda: make_move(True, 2))
attack_button_p.pack(side='top')
defense_button_p = tkinter.Button(moves_p, bg='lime green', font=('Arial', 14, 'bold'), height=1, width=18, text='DEF',
                                  command=lambda: make_move(True, 3))
defense_button_p.pack(side='top')
moves_p.pack(side='bottom')
# Computer's card
image_c = tkinter.Label(card_c, image=pokeball, width=217)
image_c.pack(side='top')
name_c = tkinter.StringVar()
stats_c = tkinter.Frame(card_c)
name_label_c = tkinter.Label(stats_c, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                             textvariable=name_c)
name_label_c.pack(side='top')
type_c = tkinter.StringVar()
type_label_c = tkinter.Label(stats_c, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                             textvariable=type_c)
type_label_c.pack(side='top')
hp_c = tkinter.StringVar()
attack_c = tkinter.StringVar()
defense_c = tkinter.StringVar()
hp_label_c = tkinter.Label(stats_c, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                           textvariable=hp_c)
hp_label_c.pack(side='top')
attack_label_c = tkinter.Label(stats_c, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                               textvariable=attack_c)
attack_label_c.pack(side='top')
defense_label_c = tkinter.Label(stats_c, anchor='w', bg='light gray', font=('Arial', 14, 'bold'), height=1, width=18,
                                textvariable=defense_c)
defense_label_c.pack(side='top')
stats_c.pack(side='top')
moves_c = tkinter.Frame(card_c)
hp_button_c = tkinter.Button(moves_c, bg='deep sky blue', font=('Arial', 14, 'bold'), height=1, width=18, text='HP')
hp_button_c.pack(side='top')
attack_button_c = tkinter.Button(moves_c, bg='red2', font=('Arial', 14, 'bold'), height=1, width=18, text='ATK')
attack_button_c.pack(side='top')
defense_button_c = tkinter.Button(moves_c, bg='lime green', font=('Arial', 14, 'bold'), height=1, width=18, text='DEF')
defense_button_c.pack(side='top')
moves_c.pack(side='bottom')

# initialisation........................................................................................................
name_p.set('Name: ')
type_p.set('Type: ')
hp_p.set('HP: ')
attack_p.set('Attack: ')
defense_p.set('Defense: ')
name_c.set('Name: ')
type_c.set('Type: ')
hp_c.set('HP: ')
attack_c.set('Attack: ')
defense_c.set('Defense: ')
update = True

# game starts...........................................................................................................
df = pd.read_csv('D:\Git\python-projects\Pokemon game\Pokemon.csv')
cards = {}
for index, row in df.iterrows():
    cards[row['Name']] = (str(row['Type 1']), int(row['HP']), int(row['Attack']), int(row['Defense']))
deck = list(cards.keys())
random.shuffle(deck)
deck_p = [deck[i] for i in range(0, len(deck)) if i % 2 == 0]
deck_c = [deck[i] for i in range(0, len(deck)) if i % 2 == 1]
del deck
cards_left_p.set('Cards left: ' + str(len(deck_p)))
cards_left_c.set('Cards left: ' + str(len(deck_c)))
show_card('player')
chance = 'player'
main_window.mainloop()

