# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import colorama
from colorama import Fore
import random
colors = list(vars(colorama.Fore).values())
from Scripts import LVM, Hadoop , Aws , Docker


if __name__ == '__main__':
    print(random.choice(colors) + "Hi Welcome to Automation World!!!!!!!!!")
    while True:
        choice = int(input(random.choice(colors) + "Which Technology You want to Use? ..... " + random.choice(colors) + "\n1.AWS\n" + random.choice(colors) + "2.Hadoop\n" + random.choice(colors) + "3.Docker\n" + random.choice(colors) + "4.LVM\n" + random.choice(colors) + "5.Exit\n" + random.choice(colors) + "Enter Choice....  " + random.choice(colors) ))
        if choice == 1:
            Aws.start()
            pass
        elif choice == 2:
            Hadoop.start()
            pass
        elif choice == 3:
            Docker.start()
            pass
        elif choice == 4:
            LVM.start()
            pass
        elif choice == 5:
            print(random.choice(colors) + "Thanks for using!!!!")
            break
        else:
            print("You entered wrong choice!!!....Please Choose Again....")
            continue




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
