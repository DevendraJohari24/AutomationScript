import subprocess , os
import socket
from colorama import Fore 

class Hadoop():
    def __init__(self, choice='D'):
        self.choice = choice
        print("\n\n\n")
        print(Fore.RED + "--------------------------------------------------------------------------------------------")
        print(Fore.RED + "||----------------------------------------------------------------------------------------||")
        print(Fore.GREEN + "||                ::    ::  ::::::::  ::::::::  ::::::::  ::::::::  ::::::::              ||")
        print(Fore.GREEN + "||                ::    ::  ::    ::   ::   ::  ::    ::  ::    ::  ::    ::              ||")
        print(Fore.BLUE + "||                ::::::::  ::::::::   ::   ::  ::    ::  ::    ::  ::::::::              ||")
        print(Fore.YELLOW + "||                ::    ::  ::    ::   ::   ::  ::    ::  ::    ::  ::                    ||")
        print(Fore.YELLOW + "||                ::    ::  ::    ::  ::::::::  ::::::::  ::::::::  ::                    ||")
        print(Fore.MAGENTA + "||----------------------------------------------------------------------------------------||")
        print(Fore.MAGENTA + "--------------------------------------------------------------------------------------------")
        print("\n\n\n")
        
            
####################################################### INSTALLATION PART ####################################################################33
    def installJava(self):
        print("......Installing Java in your respective OS......\n")
        operating = int(input("Enter type of your OS......\n1.Ubuntu \n2.Redhat\nEnter Choice...... "))
        print("\n......Changing Your Current Directory as Downloads Directory......\n")
        directory = input("Enter Directory where you downloaded your JAVA software...... ")
        os.chdir(directory)
        print(os.getcwd())
        if operating == 1:
            package_name = "openjdk-8-jdk"
            output = subprocess.run(["sudo" , "apt-get" , "install", "-y" , package_name, "--force"], check=True)
            print(output)
        elif operating == 2:
            #package_name = input("Enter the package name for Java Installation\n")
            package_name = "jdk-8u171-linux-x64.rpm"
            subprocess.run(["sudo", "rpm","-ivh",package_name, "--force"], check=True)
        try:
            subprocess.call("jps")
            print("JAVA installed successfully")
        except:
            print("There is something error in installing JAVA in your OS")
                
                
    def installHadoop(self):
        try:
            subprocess.call("jps")
            print("......Basic Requirement(JAVA) is already installed in your OS......")
        except:
            print("Your system doesn't have JAVA , so we have to install it first...INSTALLING JAVA")
            Hadoop.installJava(self)
            
        operating = int(input("Enter type of your OS......\n1.Ubuntu \n2.Redhat\nEnter Choice...... "))
        print("\n......Changing Your Current Directory as Downloads Directory......")
        directory = input("Enter Directory where you downloaded your HADOOP software...... ")
        os.chdir(directory)
        print(os.getcwd())
        if operating == 1:
            subprocess.run(["sudo", "apt-get", "install", "openssh-server", "openssh-client", "-y"],check=True)
            download_link = "https://downloads.apache.org/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz"
            subprocess.run(["wget" , download_link],check=True)
            subprocess.run(["tar" ,"xzf", "hadoop-3.2.1.tar.gz"])
            try:
                subprocess.call("hadoop")
            except:
                print("There is some error in installing Hadoop in Your System")
        elif operating == 2:
            #package_name = input("Enter the package name for Hadoop Installation")
            package_name = "hadoop-1.2.1-1.x86_64.rpm"
            subprocess.run(["sudo", "rpm","-ivh",package_name, "--force"],check=True)
            try:
                subprocess.call("hadoop")
                print("Hadoop Successfully Installed in Your System")
            except:
                print("There is some error in installing Hadoop in Your System")

######################################################################  SETUP  PART  ####################################################################################################
    """ def checkNode(self):
        choice = 1
        print("Choose One out of three Nodes -:")
        print("1. NAME NODE")
        print("2. DATA NODE")
        print("3. CLIENT")
        choice = input()
        if choice == '1':
            return 'N'
        elif choice == '2':
            return 'D'
        elif choice == '3':
            return 'C'
        else:
            print('You Entered Wrong Choice')"""


    def ChangeDirectory(self):
        print("......Moving to Hadoop Directory......")
        os.chdir('/etc/hadoop/')
        dir = os.getcwd()
        if(dir == "/etc/hadoop/"):
            print("......Directory Successfully Changed!!......")
        else:
            print("......There is some error in changing Directory!......")

    def PrintDirectoryContents(self):
        print("Printing Contents of Hadoop Directory")
        dir = os.listdir()
        for i in range(len(dir)):
            print(dir[i])

    def StartNode(self):
        if self.choice == 'N':
            print("Starting Namenode!!")
            try:
                subprocess.run(["sudo", "hadoop-daemon.sh", "start", "namenode"],check=True)
            except:
                subprocess.run(["sudo", "hadoop-daemon.sh", "stop", "namenode"],check=True)
                subprocess.run(["sudo", "hadoop-daemon.sh", "start", "namenode"],check=True)
            print("Namenode Started Running")
            subprocess.call("jps")
        elif self.choice == 'D':
            print("Starting DataNode!!")
            try:
                subprocess.run(["sudo", "hadoop-daemon.sh", "start", "datanode"],check=True)
            except:
                subprocess.run(["sudo", "hadoop-daemon.sh", "stop", "datanode"],check=True)
                subprocess.run(["sudo", "hadoop-daemon.sh", "start", "datanode"],check=True)
            print("DataNode Started Running")
            subprocess.call("jps")

    def PrintReport(self):
        print("Printing Report!!!!")
        subprocess.run(["sudo", "hadoop", "dfsadmin", "-report"], check=True)
        print("Printed Report Successfully!")

    def MasterNode(self):
        print("So We set this system as a Master Node for you!!")
        self.choice = 'N'
        Hadoop.ChangeDirectory(self)
        Hadoop.PrintDirectoryContents(self)
        print("So Now First Edit hdfs-site.xml")
        choice = 2
        choice = int(input("Do You Want to Setup folder by 1. yours  OR 2. default:  "))
        if choice == 1:
            folder = input("Enter the location of folder that u created for NameNode:  ")
            try:
                subprocess.run(["sudo", "mkdir",folder], check=True)
                print("Folder created successfully in your respective location......")
            except:
                print("Folder found successfully in your respective location......")
            value = "<value>" + folder + "</value>"
        else:
            print("......Creating New Folder with name 'nn' at root directory......")
            try:
                subprocess.run(["sudo","mkdir","/nn" ], check=True)
            except:
                pass
            value = "<value>" + "/nn" + "</value>"
        f = open("hdfs-site.xml", "w+")
        contents = ["<configuration>", "<property>" ,"<name>dfs.name.dir</name>", value ,"</property>" ,"</configuration>"]
        for i in range(len(contents)):
            f.write(contents[i])
            f.write("\n")
        f.close()
        print("Editing hdfs-site.xml file Completed...")
        f = open("hdfs-site.xml", "r")
        if f.mode == "r":
            contents = f.read()
            print(contents)

        print("Now Editing core-site.xml file")
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        value = "<value>" + "hdfs://" + IPAddr + ":9001" + "</value>"
        f = open("core-site.xml", "w+")
        contents = ["<configuration>", "<property>", "<name>fs.default.name</name>", value, "</property>",
                    "</configuration>"]
        for i in range(len(contents)):
            f.write(contents[i])
            f.write("\n")
        f.close()
        print("Editing core-site.xml file Completed...")
        f = open("core-site.xml", "r")
        if f.mode == "r":
            contents = f.read()
            print(contents)
        ##################### FORMATING NAMENODE ######################
        print("Formating the Folder of Namenode You Created!")
        print(self.choice)
        try:
            subprocess.run(["hadoop", "namenode", "-format", "-y"], check=True)
        except:
            print("There is some Error in Formatting NameNode Folder")
        
        print("Starting Hadoop for Name Node......")
        Hadoop.StartNode(self)

    def DataNode(self):
        print("So We set this system as a Data Node for you!!")
        self.choice = 'D'
        Hadoop.ChangeDirectory(self)
        Hadoop.PrintDirectoryContents(self)
        print("So Now First Edit hdfs-site.xml")
        choice = 2
        choice = int(input("Do You Want to Setup folder by 1. yours  OR 2. default :   "))
        if choice == 1:
            folder = input("Enter the location of folder that u created for NameNode:   ")
            try:
                subprocess.run(["sudo", "mkdir",folder], check=True)
                print("Folder created successfully in your respective location......")
            except:
                print("Folder found successfully in your respective location......")
            value = "<value>" + folder + "</value>"
        else:
            print("......Creating New Folder with name 'dn' at root directory......")
            try:
                subprocess.run(["sudo","mkdir","/dn" ], check=True)
            except:
                pass
            value = "<value>" + "/dn" + "</value>"
        f = open("hdfs-site.xml", "w+")
        contents = ["<configuration>", "<property>", "<name>dfs.data.dir</name>", value, "</property>",
                    "</configuration>"]
        for i in range(len(contents)):
            f.write(contents[i])
            f.write("\n")
        f.close()
        print("Editing hdfs-site.xml file Completed...")
        f = open("hdfs-site.xml", "r")
        if f.mode == "r":
            contents = f.read()
            print(contents)

        print("Now Editing core-site.xml file")
        IPAddr = input("Enter the IP Address of NameNode")
        value = "<value>" + "hdfs://" + IPAddr + ":9001" + "</value>"
        f = open("core-site.xml", "w+")
        contents = ["<configuration>", "<property>", "<name>fs.default.name</name>", value, "</property>",
                    "</configuration>"]
        for i in range(len(contents)):
            f.write(contents[i])
            f.write("\n")
        f.close()
        print("Editing core-site.xml file Completed...")
        f = open("core-site.xml", "r")
        if f.mode == "r":
            contents = f.read()
            print(contents)
        Hadoop.StartNode(self)


    def Client(self):
        print("So We set this system as a Client for you!!")
        Hadoop.ChangeDirectory(self)
        Hadoop.PrintDirectoryContents(self)

        print("Now Editing core-site.xml file")

        IPAddr = input("Enter the IP Address of NameNode...... ")
        value = "<value>" + "hdfs://" + IPAddr + ":9001" + "</value>"
        f = open("core-site.xml", "w+")
        contents = ["<configuration>", "<property>", "<name>fs.default.name</name>", value, "</property>",
                    "</configuration>"]
        for i in range(len(contents)):
            f.write(contents[i])
            f.write("\n")
        f.close()
        print("Editing core-site.xml file Completed...")
        f = open("core-site.xml", "r")
        if f.mode == "r":
            contents = f.read()
            print(contents)

    def ClientOperation(self):
        print("Select which Operation do you want to Perform on Your Hadoop Cluster?")
        print("1. Listing All the items in Particular Directory!")
        print("2. Read a Particular File ")
        print("3. Create a new Directory")
        print("4. Create a new file")
        print("5. Remove a Directory")
        print("6. Remove a Particular File")
        print("7. Custom Operation.....")
        choice = int(input())
        if choice == 1:
            path = input("Enter Directory which you want to see")
            subprocess.run(["sudo","hadoop" ,"fs" , "-ls" ,path],check=True)
        elif choice == 2:
            name = input("Enter Name of file which you want to read")
            subprocess.run(["sudo","hadoop" ,"fs" , "-cat" ,name],check=True)

        elif choice == 3:
            directory_name = input("Enter Directory name")
            subprocess.run(["sudo","hadoop" ,"fs" , "-mkdir" ,directory_name],check=True)

        elif choice == 4:
            file_name = input("Enter Directory which you want to see")
            subprocess.run(["sudo","hadoop" ,"fs" , "-touch" ,file_name],check=True)

        elif choice == 5:
            directory = input("Enter Directory which you want to delete")
            subprocess.run(["sudo", "hadoop", "fs", "-rm", "-rf", directory], check=True)

        elif choice == 6:
            file = input("Enter file name which you want to deleted")
            subprocess.run(["sudo", "hadoop", "fs", "-rm", file], check=True)
        elif choice == 7:
            cmd = input("Input Custom Hadoop Command!")
            subprocess.run(["sudo", cmd],check = True)


if __name__ == '__main__':
    h = Hadoop()
    choice = -1
    while True:
        choice = int(input(Fore.WHITE + "Enter what do you want \n1.Install Hadoop in your System\n2.Setup Name Node\n3.Setup Data Node\n4.Setup Client\n5.Showing Node Report\n6.Performing Client Operations\n7.Exit\nEnter Choice ...."))
        if choice == 1:
            print("......Installing Hadoop in your OS......")
            h.installHadoop()
        elif choice == 2:
            print("......Setuping NameNode......")
            h.MasterNode()
        elif choice == 3:
            print ("......Setuping DataNode......")
            h.DataNode()
        elif choice == 4:
            print ("......Setuping Client......")
            h.Client()
        elif choice == 5:
            print ("......Showing Reports......")
            h.PrintReport()
        elif choice == 6:
            print ("......Showing Client Operations......")
            h.ClientOperation()
        elif choice == 7:
            print("......Exiting......")
            break