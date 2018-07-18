import data
import sys

def pronounce(number):
    '''pronounces any number having less than 4 digits except 000
    ie. 002 - two, 020 - twenty, 200 - two hundred, 123 - one hundred twenty three, 000 - <print_nothing>'''
    if number[0] != '0':
        print(data.pronounce[int(number[0])], end = ' ')
        print("hundred", end = ' ')
    if int(number[1:]) == 0:
        return
    if int(number[1:]) in data.pronounce:
        print(data.pronounce[int(number[1:])], end = ' ')
    else:
        print(data.pronounce[int(number[1]) * 10], end = ' ')
        print(data.pronounce[int(number[2])], end = ' ')
    return

if len(sys.argv) != 2:
    print("Invalid usage")
    print("Usage: numberpronounce.py    number_argument")
    print("number_argument can be any integer or floating point number")
    print("ie. numberpronounce.py   123.4")
else:
    try:
        number = float(sys.argv[1])
    except ValueError:
        print("Invalid argument")
        sys.exit(1)
    numbers = str(number).split('.')
    number = numbers[0]
    base = len(number)
    
    if base % 3 == 1:
        number = "00" + number
        base += 2

    elif base % 3 == 2:
        number = "0" + number
        base += 1

    pos = base // 3
    if int(number) == 0:
        print('zero', end = ' ')
    else:
        while pos :
            if int(number) == 0:
                break
            pronounce(number[0:3])
            number = number[3:]
            print(data.position[pos], end =' ')
            pos -= 1

    if int(numbers[1]) != 0:
        print("point", end = ' ')
        number = numbers[1]
        for c in number:
            print(data.pronounce[int(c)], end = ' ')
    print('')