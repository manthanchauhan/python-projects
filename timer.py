import sys
import msvcrt
import winsound
from time import sleep
l = len(sys.argv)
if l != 3:
    print("invalid use")
    print("Usage: timer.py timer_duration")
    print("write timer_duration as 15 m, 60 s or 1 h")
    print("ie. timer.py 10 s")
    print("press Ctrl + C to interrupt timer")
    print("press any key to stop buzzer after timer completes")
else:
    try:
        time = int(sys.argv[1])
    except ValueError:
        print ("invalid time")
        sys.exit(1)
    
    if time < 0:
        print("invalid time")
        sys.exit(1)
    
    unit = sys.argv[2]
    if unit == 'm':
        time *= 60
        end_word = "minute"
    elif unit == 'h':
        time *= 3600
        end_word = "hour"
    elif unit == 's':
        end_word = "second"
    else:
        print("invalid time")
        sys.exit(1)

    if int(sys.argv[1]) != 1:
        end_word = end_word + "s"
    print("timer set for %d "%(int(sys.argv[1])) + end_word)
    try:
        sleep(time)
        while True:
            if msvcrt.kbhit():
                k = msvcrt.getch()
                print("timer stopped")
                sys.exit(1)
            else:
                winsound.Beep(500, 1000)
                sleep(0.01)
    except KeyboardInterrupt:
        print("timer interrupted")
        sys.exit(1)
