#!/usr/bin/env python
# coding: utf-8

import pyttsx3
import datetime
import speech_recognition as sr
import subprocess
import shutil
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def usrname():
    speak("What should i call you sir")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")

    assname = ("Alexa")
    speak("I am your Assistant")
    speak(assname)


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognizing your voice.")
        return "None"

    return query


class LVM:
    def __init__(self, size="", disk_name="", source_name="", mount_folder="", increase_size="", decrease_size="", hd_name=""):
        self.__size = size
        self.__disk_name = disk_name
        self.__source_name = source_name
        self.__mount_folder = mount_folder
        self.__increase_size = increase_size
        self.__decrease_size = decrease_size
        self.__hd_name = hd_name

    def createPhysicalPartition(self):
        speak("What is the name of partition")
        self.__hd_name = takeCommand()
        subprocess.run("sudo pvcreate " + "/dev/" + self.__hd_name)
        output = subprocess.run("sudo pvdisplay " + "/dev/" + self.__hd_name)
        print(output)

    def createVisualPartition(self):
        speak("What is name of the first hard disk")
        storage1 = takeCommand()
        speak("What is name of the second hard disk")
        storage2 = takeCommand()
        speak("What is the name of virtual hard disk")
        self.__source_name = takeCommand()
        subprocess.run("sudo vgcreate " + self.__source_name + "/dev/" + storage1 + "  /dev/" + storage2)
        output = subprocess.run("sudo vgdisplay " + self.__source_name)
        print(output)


    def createLVMPartition(self):
        speak("What is the size of partition which you want to create?")
        self.__size = takeCommand()
        speak("What is the disk name ")
        self.__disk_name = takeCommand()
        speak("What is the source disk name ")
        self.__source_name = takeCommand()
        subprocess.run("sudo lvcreate --size " + self.__size + "G" + " --name " + self.__disk_name + " " + self.__source_name)
        output = subprocess.run("sudo lvdisplay " + self.__source_name + "/" + self.__disk_name)
        print(output)

    def formatPartition(self):
        speak("Now Formatting Your Partition")
        output = subprocess.run("sudo mkfs.ext4 " + "/dev/" + self.__source_name + "/" + self.__disk_name)
        print(output)

    def mountPartition(self):
        speak("Now Mount the Partition")
        speak("What is the name of mount folder")
        self.__mount_folder = takeCommand()
        output = subprocess.run("sudo mount " + "/dev/" + self.__source_name + "/" + self.__disk_name + " " + "/" + self.__mount_folder)
        print(output)

    def increasePartition(self):
        speak("How much you want to extend the partition")
        self.__increase_size = takeCommand()
        subprocess.run("sudo lvextend --size +" + self.__increase_size + "G " + "/dev/" + self.__source_name + "/" + self.__disk_name)
        subprocess.run("sudo resize2fs /dev/" + self.__source_name + "/" + self.__disk_name)

    def decreasePartition(self):
        speak("How much you want to decrease the partition")
        self.__decrease_size = takeCommand()
        subprocess.run("sudo lvextend --size -" + self.__decrease_size + "G " + "/dev/" + self.__source_name + "/" + self.__disk_name)
        subprocess.run("sudo resize2fs /dev/" + self.__source_name + "/" + self.__disk_name)

    def showPartition(self):
        speak("Partitions are as following")
        output = subprocess.run("sudo df -h")
        print(output)
    
    def extendPartition(self):
        speak("What is tha name of partition you extended")
        extended_partition = takeCommand()
        subprocess.run("sudo vgextend " + self.__source_name + " /dev/" + extend_partition)


if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    usrname()
    l = LVM()
    
    while True:
        speak("Heyy!..What do you want to do ?")
        query = takeCommand().lower()
        if (query.find(('create' and 'physical') or 'partition')) == -1:
            l.createPhysicalPartition()
        elif (query.find(('create' and 'virtual') or 'partition')) == -1:
            l.createVisualPartition()
        elif (query.find(('create' and 'lvm') or 'partition')) == -1:
            l.createLVMPartition()
            l.formatPartition()
            l.mountPartition()
        elif (query.find('increase' or 'size' or 'partition')) == -1:
            l.increasePartition()
        elif (query.find('decrease' or 'size' or 'partition')) == -1:
            l.decreasePartition()
        elif (query.find('extend' and 'partition')) == -1:
            l.decreasePartition()
        elif (query.find('show' or 'lvm' or 'partition')) == -1:
            l.showPartition()






