import subprocess
import shutil
import os
import colorama
from colorama import Fore
import random

colors = list(vars(colorama.Fore).values())

class LVM():
    def __init__(self, size=0, disk_name="", source_name="", mount_folder="", increase_size=0, decrease_size=0, hd_name=""):
        self.__size = size
        self.__disk_name = disk_name
        self.__source_name = source_name
        self.__mount_folder = mount_folder
        self.__increase_size = increase_size
        self.__decrease_size = decrease_size
        self.__hd_name = hd_name
        print("\n\n\n")
        print(random.choice(colors)+"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(random.choice(colors)+"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(random.choice(colors)+"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(random.choice(colors)+"++++                                                                                  ++++")
        print(random.choice(colors)+"++++              +++          +++            +++     ++++++       ++++++             ++++")
        print(random.choice(colors)+"++++              +++           +++          +++      +++  +++    +++ +++             ++++")
        print(random.choice(colors)+"++++              +++            +++       +++        +++   +++  +++  +++             ++++")
        print(random.choice(colors)+"++++              +++             +++     +++         +++    ++++++   +++             ++++")
        print(random.choice(colors)+"++++              +++              +++   +++          +++             +++             ++++")
        print(random.choice(colors)+"++++              ++++++++++        ++ + ++           +++             +++             ++++")
        print(random.choice(colors)+"++++              ++++++++++        ++++++            +++             +++             ++++")
        print(random.choice(colors)+"++++                                                                                  ++++")
        print(random.choice(colors)+"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(random.choice(colors)+"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(random.choice(colors)+"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("\n\n\n")

    def showUnusedStorage(self):
        print("---------------------------------------SHOWING PARTITIONS------------------------------------------")
        print("Showing all partitions in your OS....")
        subprocess.run(["fdisk","-l"], check=True)


    def createPhysicalPartition(self):
        print("------------------------------------CREATING PHYSICAL PARTITION-------------------------------------")
        print("What is the name of partition")
        self.__hd_name = input()
        name = "/dev/"+ self.__hd_name
        subprocess.run(["pvcreate" , name],check=True)
        output = subprocess.run(["pvdisplay", name], check=True)
        print(output)

    def createVisualPartition(self):
        print("------------------------------------CREATING VIRTUAL PARTITION-------------------------------------")
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
        print("----------------------------- CREATING LVM PARTITION ------------------------------------------")
        self.__size = int(input("What is the size of partition which you want to create?"))
        print("What is the disk name ")
        size = str(self.__size) + "G"
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
        print("-----------------------------INCREASING PARTITION-----------------------------")
        self.__increase_size = int(input("How much you want to extend the partition?... "))
        size =  "+" + str(self.__increase_size) + "G"
        self.__source_name = input("Enter source partition name... ")
        self.__disk_name = input("Enter disk name.. ")
        name = "/dev/" + self.__source_name + "/" + self.__disk_name
        print("------------------------------EXTEND FILE SYSTEM-------------------------")
        subprocess.run(["lvextend" , "--size", size , name], check=True)
        print("-----------------------------CHECK FILE SYSTEM--------------------------")
        subprocess.run(["resize2fs",name], check=True)

    def decreasePartition(self):
        print("----------------------------DECREASING PARTITION---------------------")
        #STEPS
        #unmount the file system for reducing.
        #check the file system after unmount.
        #Reduce the file system.
        #Reduce the Logical Volume size than Current size.
        #Recheck the file system for error.
        #Remount the file-system back to stage.
        self.__decrease_size = int(input("How much do you want to reduce the partition?... "))
        print("-----------------------UNMOUNTING FILE-SYSTEM---------------------")
        foldername = "/" + self.__mount_folder
        subprocess.run(["umount","-v", foldername],check=True)
        name = "/dev/" + self.__source_name + "/" + self.__disk_name
        print("------------------------CHECK FILE SYSTEM------------------------")
        subprocess.run(["e2fsck","-ff" , name],check=True)
        size = str(self.__size - self.__decrease_size) + "G"
        print("-------------------------REDUCE FILE SYSTEM-----------------------")
        subprocess.run(["resize2fs",name,size],check=True)
        decreasedsize = "-" + str(self.__decrease_size) + "G"
        print("-------------------------REDUCE LOGICAL VOLUME---------------------")
        subprocess.run(["lvreduce", "-L",decreasedsize , name ],check=True)
        subprocess.run(["lvdisplay",self.__disk_name],check=True)
        print("--------------------------RECHECK FILE SYSTEM----------------------")
        subprocess.run(["resize2fs", name],check=True)
        print("--------------------------MOUNT FILE-SYSTEM-------------------------")
        subprocess.run(["mount", name , foldername],check=True)
        subprocess.run(["lvdisplay",self.__disk_name],check=True)
   

        


    def showPartition(self):
        print("Partitions are as following")
        output = subprocess.run(["df", "-h"],check=True)
        print(output)


if __name__ == '__main__':
    l = LVM()
    while True:
        print(random.choice(colors) + "Select What do you want....." + random.choice(colors) + "\n1.Show all Partitions\n" + random.choice(colors) + "2.Create Physical Partition\n" + random.choice(colors) + "3.Create Visual Partition\n" + random.choice(colors) + "4.Create LVM Partition\n" + random.choice(colors) + "5.Increase Partition Size\n" + random.choice(colors) +"6.Decrease Partition Size\n" + random.choice(colors) +"7.Show LVM Partition\n" + random.choice(colors) + "8.Exit\n" + random.choice(colors) + "Enter Choice...." + random.choice(colors))
        choice = int(input())
        if choice == 1:
            print(random.choice(colors))
            l.showUnusedStorage()
        elif choice == 2:
            print(random.choice(colors))
            l.createPhysicalPartition()
        elif choice == 3:
            print(random.choice(colors))
            l.createVisualPartition()
        elif choice == 4:
            print(random.choice(colors))
            l.createLVMPartition()
        elif choice == 5:
            print(random.choice(colors))
            l.increasePartition()
        elif choice == 6:
            print(random.choice(colors))
            l.decreasePartition()
        elif choice == 7:
            print(random.choice(colors))
            l.showPartition()
        elif choice == 8:
            print(random.choice(colors) + "----------------------------------------EXITING--------------------------------------")
            break
