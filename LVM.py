import subprocess
import shutil
import os
from colorama import Fore

class LVM():
    def __init__(self, size="", disk_name="", source_name="", mount_folder="", increase_size="", decrease_size="", hd_name=""):
        self.__size = size
        self.__disk_name = disk_name
        self.__source_name = source_name
        self.__mount_folder = mount_folder
        self.__increase_size = increase_size
        self.__decrease_size = decrease_size
        self.__hd_name = hd_name
        print("\n\n\n")
        print(Fore.RED +"\ " + Fore.GREEN +  "/" + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED +  "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN  + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED  + "\ " + Fore.GREEN +  "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED +"\ " + Fore.GREEN +  "/")
        print(Fore.GREEN + "\                                                                    /")
        print(Fore.RED + "\             ::          ::        ::      :::      :::             /")
        print(Fore.GREEN + "\             ::           ::      ::       :: ::  :: ::             /")
        print(Fore.RED + "\             ::            ::    ::        ::   ::   ::             /")
        print(Fore.GREEN + "\             ::              :: ::         ::        ::             /")
        print(Fore.RED + "\             ::::::::         ::           ::        ::             /")
        print(Fore.GREEN + "\                                                                    /")
        print(Fore.RED +"\ " + Fore.GREEN +  "/" + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED +  "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN  + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED  + "\ " + Fore.GREEN +  "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED + "\ " + Fore.GREEN + "/ " + Fore.RED +"\ " + Fore.GREEN +  "/")
        print("\n\n\n")

    def showUnusedStorage(self):
        print("Showing all partitions in your OS....")
        subprocess.run(["fdisk","-l"], check=True)


    def createPhysicalPartition(self):
        print("What is the name of partition")
        self.__hd_name = input()
        name = "/dev/"+ self.__hd_name
        subprocess.run(["pvcreate" , name],check=True)
        output = subprocess.run(["pvdisplay", name], check=True)
        print(output)

    def createVisualPartition(self):
        print("What is name of the first hard disk")
        storage1 = input()
        print("What is name of the second hard disk")
        storage2 = input()
        print("What is the name of virtual hard disk")
        self.__source_name = input()
        name1 =  "/dev/" + storage1
        name2 =  "/dev/" + storage2
        subprocess.run(["vgcreate" , self.__source_name , name1 , name2], check=True)
        output = subprocess.run(["vgdisplay" ,self.__source_name], check=True)
        print(output)


    def createLVMPartition(self):
        print("----------------------------- CREATING PARTITION ------------------------------------------")
        print("What is the size of partition which you want to create?")
        self.__size = input()
        print("What is the disk name ")
        size = self.__size + "G"
        self.__disk_name = input()
        print("What is the source disk name ")
        self.__source_name = input()
        name = self.__source_name + "/" + self.__disk_name
        subprocess.run(["lvcreate", "--size" ,size,"--name", self.__disk_name ,self.__source_name],check=True)
        output = subprocess.run(["lvdisplay", name], check=True)
        print(output)
        print("------------------------------ FORMATTING PARTITION ------------------------------------------")
        LVM.formatPartition(self)

    def formatPartition(self):
        print("Now Formatting Your Partition")
        name =  "/dev/" + self.__source_name + "/" + self.__disk_name
        output = subprocess.run(["mkfs.ext4", name], check=True)
        print(output)
        print("------------------------------ MOUNT PARTITION ----------------------------------------------")
        LVM.mountPartition(self)

    def mountPartition(self):
        print("Now Mount the Partition")
        print("What is the name of mount folder")
        self.__mount_folder = input()
        name = "/dev/" + self.__source_name + "/" + self.__disk_name
        foldername = "/" + self.__mount_folder
        try:
            subprocess.run(["mkdir", foldername], check=True)
            print("Mounting Folder successfully created")
        except:
            print("Mounting Folder successfully found")
        output = subprocess.run(["mount", name, foldername], check=True)
        print(output)
        print("--------------------- SUCCESSFULLY DONE ALL THREE STEPS ------------------------------------")

    def increasePartition(self):
        print("How much you want to extend the partition")
        self.__increase_size = input()
        size =  "+" + self.__increase_size + "G"
        self.__source_name = input("Enter source partition name... ")
        self.__disk_name = input("Enter disk name.. ")
        name = "/dev/" + self.__source_name + "/" + self.__disk_name
        subprocess.run(["lvextend" , "--size", size , name], check=True)
        subprocess.run(["resize2fs",name], check=True)

    def showPartition(self):
        print("Partitions are as following")
        output = subprocess.run(["df", "-h"],check=True)
        print(output)


if __name__ == '__main__':
    clear = lambda: os.system('cls')

    # This Function will clean any
    # command before execution of this python file
    clear()
    l = LVM()
    while True:
        print("Select What do you want.....\n1.Show all Partitions\n2.Create Physical Partition\n3.Create Visual Partition\n4.Create LVM Partition\n5.Increase Partition Size\n6.Show LVM Partition\n7.Exit\nEnter Choice....")
        choice = int(input())
        if choice == 1:
            l.showUnusedStorage()
        elif choice == 2:
            l.createPhysicalPartition()
        elif choice == 3:
            l.createVisualPartition()
        elif choice == 4:
            l.createLVMPartition()
        elif choice == 5:
            l.increasePartition()
        elif choice == 6:
            l.showPartition()
        elif choice == 7:
            break
