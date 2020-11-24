import subprocess
import json
import spur
import os
import getpass
import colorama
from colorama import Fore
import random

colors = list(vars(colorama.Fore).values())

class AWS():
    def __init__(self, ami_type="",instance_type="",no_of_instance=1,vpc="", cidr="10.0.0.0/16",vpc_id="",igw="",route_table_id="",cidr_subnet=[],key_name="",sg_id="",ebs_vol_id="", instance_id="",s3_location="",instance_ids=[],domain_name="",root_object="", bucket_name="",region=""):
        print("\n\n\n")
        print(Fore.YELLOW + "||------------------------------------------||")
        print(Fore.BLUE + "||------------------------------------------||")
        print(Fore.YELLOW + "||  :::::::     ::          ::     :::::::  ||")
        print(Fore.BLUE + "||  ::   ::      ::        ::      ::       ||")
        print(Fore.YELLOW + "||  :::::::       ::  ::  ::       :::::::  ||")
        print(Fore.BLUE + "||  ::   ::        :: :: ::             ::  ||")
        print(Fore.YELLOW + "||  ::   ::         ::::::         :::::::  ||")
        print(Fore.BLUE + "||------------------------------------------||")
        print(Fore.YELLOW +"||------------------------------------------||" + Fore.WHITE)
        print("\n\n\n")
        self.ami_type = ami_type
        self.instance_type = instance_type
        self.no_of_instance = no_of_instance
        self.vpc = vpc
        self.cidr = cidr
        self.vpc_id = vpc_id
        self.igw = igw
        self.route_table_id = route_table_id
        self.cidr_subnet = cidr_subnet
        self.key_name = key_name
        self.sg_id = sg_id
        self.ebs_vol_id = ebs_vol_id
        self.instance_id = instance_id
        self.s3_location = s3_location
        self.instance_ids = instance_ids
        self.domain_name = domain_name
        self.root_object = root_object
        self.bucket_name = bucket_name
        self.region = region

    def installJSON(self):
        print(random.choice(colors) + "----------------------------INSTALLING JQ--------------------------------")
        try:
            subprocess.run(["jq","--help"],check=True)
            print("You already have jq installed in your system.....")
        except:
            subprocess.run(["sudo", "apt-get","install","jq"], check=True)
            print("Jq installed successfully in your system.....")

    def installAWSCliV2(self):
        print(random.choice(colors) + "----------------------------INSTALLING AWS-------------------------------")
        try:
            subprocess.run(["aws", "--version"], check=True)
            print("AWS already configured in your system......")
        except:
            downloading_link = "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
            folder_name = "awscliv2.zip"
            subprocess.run(["curl", downloading_link, "-o", folder_name],check=True)
            subprocess.run(["unzip", "awscliv2.zip"],check=True)
            subprocess.run(["./aws/install"], check=True)
            print(random.choice(colors) + "-------------------SUCCESSFULLY INSTALLED----------------------------")
            AWS.installJSON(self)

    
    def AWSConfigure(self):
        print(random.choice(colors) + "--------------------------CONFIGURING AWS--------------------------------")
        print("Enter Credientials........")
        try:
            subprocess.run(["aws", "configure"], check=True)
        except:
            print(random.choice(colors) + "-------------AWS NOT CONFIGURED IN YOUR SYSTEM----------------")
            AWS.installAWSCliV2(self)
            subprocess.run(["aws", "configure"], check=True)
        print("-------------------------AWS CONFIGURED SUCCESSFULLY---------------------")

    def SelectAMIimage(self):
        print(random.choice(colors) + "------------------------SELECTING AMI IMAGE-------------------------")
        choice = int(input("Select One AMI image in follwing images ---------->\n1.Amazon Linux 2 AMI (HVM), SSD Volume Type\n2.Red Hat Enterprise Linux 8 (HVM), SSD Volume Type\n3.Ubuntu Server 20.04 LTS (HVM), SSD Volume Type\n4.Microsoft Windows Server 2019 Base \n5.SUSE Linux Enterprise Server 15 SP2 (HVM), SSD Volume Type\n6.Custom Input\nEnter Choice... "))
        if choice == 1:
            self.ami_type = "ami-0e306788ff2473ccb"
        elif choice == 2:
            self.ami_type = "ami-0a9d27a9f4f5c0efc"
        elif choice == 3:
            self.ami_type = "ami-0a4a70bd98c6d6441"
        elif choice == 4:
            self.ami_type = "ami-0b2f6494ff0b07a0e"
        elif choice == 5:
            self.ami_type = "ami-0d0522ed4db1debd6"
        elif choice == 6:
            self.ami_type = input("Enter Custom AMI image.... ")

    def InstanceType(self):
        print(random.choice(colors) + "---------------------------SELECTING INSTANCE TYPE------------------------")
        choice = int(input("Select One Instane type in following ----->\n1.t2.nano\n2.t2.micro[FREE]\n3.t2.small\n4.t2.medium\n5.t2.large\n6.Custom Instance type\nEnter Choice.... "))
        if choice == 1:
            self.instance_type = "t2.nano"
        elif choice == 2:
            self.instance_type = "t2.micro"
        elif choice == 3:
            self.instance_type = "t2.small"
        elif choice == 4:
            self.instance_type = "t2.medium"
        elif choice == 5:
            self.instance_type = "t2.large"
        elif choice == 6:
            self.instance_type = input("Enter Custom Instance Type... ")

    def CreateSecurityGroup(self):
        print(random.choice(colors) + "----------------------------CREATING SECURITY GROUP--------------------------")
        choice = int(input("Which Security Group Do you want to use?...\n1.PreCreated\n2.New One\nEnter Choice.... "))
        if choice == 1:
            security_group = input("Enter Security Group Name... ")
            file_= open("security_group_output.json",'w+')
            subprocess.run(["aws", "ec2", "describe-security-groups", "--group-names",security_group],check=True,stdout=file_)
            file_.close()
            file = open("security_group_id.txt", 'w+')
            subprocess.run(["jq",".SecurityGroups[0].GroupId", "security_group_output.json"],check=True,stdout=file)
            file.close()
            file = open("security_group_id.txt",'r+')
            for x in file:
                print(x[1:-2])
                self.sg_id = x[1:-2]
            file.close()
            subprocess.run(["rm","security_group_output.json","security_group_id.txt","-f"],check=True)


        elif choice == 2:
            group_name = input("Enter Group Name... ")
            description = input("Enter Description for your Security Group... ")
            file_ = open('security_group.json', 'w+')
            subprocess.run(["aws" ,"ec2" ,"create-security-group" ,"--group-name" ,group_name ,"--description", description ,"--vpc-id", self.vpc_id],check=True, stdout=file_)
            file_.close()
            file = open('security_group_id.txt', 'w+')
            subprocess.run(["jq", ".GroupId", "security_group.json"], check=True, stdout=file)
            file.close()
            file = open('security_group_id.txt', 'r+')
            for x in file:
                print(x[1:-2])
                self.sg_id = x[1:-2]
            file.close()
            subprocess.run(["rm","security_group.json","security_group_id.txt","-f"],check=True)
            protocol = input("Enter Protocol for your Security Group... ")
            port = input("Enter Port No for your Security Group... ")
            cidr = input("Enter CIDR block for your Security Group... ")
            print(random.choice(colors) + "-----------------------------AUTHORIZING SECURITY GROUP---------------------------")
            subprocess.run(["aws","ec2","authorize-security-group-ingress" ,"--group-id",self.sg_id ,"--protocol", protocol, "--port" , port, "--cidr" , cidr],check=True)


    def CreateKeyPair(self):
        print(random.choice(colors) + "--------------------------CREATING KEY PAIR------------------------------")
        choice = int(input("Which Key do you want to use?\n1.PreCreated\n2.Create a New One.\nEnter Choice...."))
        if choice == 1:
            self.key_name = input("Enter PreCreated KeyPair Name... ")
        elif choice == 2:
            self.key_name = input("Enter KeyName for Keypair... ")
            file_ = open(f'{self.key_name}.pem', 'w+')
            subprocess.run(["aws", "ec2" ,"create-key-pair" ,"--key-name" ,self.key_name , "--query" ,"KeyMaterial" ,"--output" ,"text" ],check=True, stdout=file_)
            file_.close()
            print(random.choice(colors) + "--------------------------Changing KEY-FILE PERMISSIONS------------------------")
            key_filename = self.key_name + ".pem"
            subprocess.run(["sudo", "chmod", "400", key_filename],check=True)

    def CreateRouteTable(self):
        print(random.choice(colors) + "---------------------------CREATING ROUTE TABLE-----------------------------")
        file_ = open('route_table.json', 'w+')
        subprocess.run(["aws","ec2","create-route-table","--vpc-id",self.vpc_id], check=True, stdout=file_)
        file_.close()
        file = open('route_table_id.txt', 'w+')
        subprocess.run(["jq", ".RouteTable.RouteTableId", "route_table.json"], check=True, stdout=file)
        file.close()
        file = open('route_table_id.txt', 'r+')
        for x in file:
            print(x[1:-2])
            self.route_table_id = x[1:-2]
        file.close()
        subprocess.run(["rm","route_table.json","route_table_id.txt","-f"],check=True)

        print(random.choice(colors) + "---------------------------ATTACHING ROUTE TABLE-----------------------------")
        destination_cidr_block=""
        choice = int(input("Enter Destination CIDR Block....\nDo you want to make it by \n1.Default[0.0.0.0/0]\n2.Custom\nEnter Choice... "))
        if choice == 1:
            destination_cidr_block = "0.0.0.0/0"
        elif choice == 2:
            destination_cidr_block = input("Enter Custom Destination CIDR Block.. ")
        subprocess.run(["aws","ec2","create-route","--route-table-id",self.route_table_id,"--destination-cidr-block",destination_cidr_block,"--gateway-id", self.igw],check=True)
        print(random.choice(colors) + "--------------------------CHOOSE SUBNET FOR ROUTE TABLE------------------------")
        print("You have created following Subnets -: ")
        for i in range(len(self.cidr_subnet)):
            print(str(i+1) + "--->" + self.cidr_subnet[i])
        while choice == 1:
            print(random.choice(colors) + "---------------------------ASSOCIATING SELECTED SUBNET TO ROUTE TABLE----------------------------")
            ch = int(input("Choose one of the above subnets... "))
            print(ch)
            print(self.cidr_subnet[ch-1])
            subprocess.run(["aws" ,"ec2", "associate-route-table" ,"--subnet-id" ,self.cidr_subnet[ch-1] ,"--route-table-id" ,self.route_table_id],check=True)
            choice = int(input("Do you want to associate more subnets..\n1.Yes\n2.No\nEnter Choice.. "))

    def CreateInternetGateway(self):
        print(random.choice(colors) + "----------------------------CREATING INTERNET GATEWAY------------------------")
        file_ = open('igw.json', 'w+')
        subprocess.run(["aws","ec2","create-internet-gateway"],check=True,stdout=file_)
        file_.close()
        file = open('igw_id.txt', 'w+')
        subprocess.run(["jq", ".InternetGateway.InternetGatewayId", "igw.json"], check=True, stdout=file)
        file.close()
        file = open('igw_id.txt', 'r+')
        for x in file:
            print(x[1:-2])
            self.igw = x[1:-2]
        file.close()
        subprocess.run(["rm","igw.json","igw_id.txt","-f"],check=True)

        print(random.choice(colors) + "----------------------------ATTACHING INTERNET GATEWAY-----------------------")
        subprocess.run(["aws", "ec2", "attach-internet-gateway", "--vpc-id", self.vpc_id, "--internet-gateway-id", self.igw],check=True)
        AWS.CreateRouteTable(self)


    def CreateSubnet(self):
        print(random.choice(colors) + "----------------------------CREATING SUBNET----------------------------------")
        choice = 1
        while choice == 1:
            cidr_subnet = input("Enter cidr block value.. ")
            file_ = open('subnet.json','w+')
            subprocess.run(["aws","ec2","create-subnet","--vpc-id",self.vpc_id, "--cidr-block",cidr_subnet], check=True,stdout=file_)
            file_.close()
            file = open('subnet_id.txt', 'w+')
            subprocess.run(["jq", ".Subnet.SubnetId" ,"subnet.json"], check=True, stdout=file)
            file.close()
            file = open('subnet_id.txt','r+')
            for x in file:
                print(x[1:-2])
                self.cidr_subnet.append(x[1:-2])
            file.close()
            subprocess.run(["rm","subnet.json","subnet_id.txt","-f"],check=True)
            choice = int(input("Do you want to create more Subnets..?\n1.Yes\n2.No\nEnter Choice.. "))

        AWS.CreateInternetGateway(self)     

    def CreateVPC(self):
        print(random.choice(colors) + "----------------------CREATING VIRTUAL PRIVATE CLOUD-----------------------")
        self.cidr = input("Enter CIDR Block.... ")
        file_ = open('vpc_output.json', 'w+')
        subprocess.run(["aws", "ec2","create-vpc", "--cidr-block",self.cidr], check=True,stdout=file_)
        file_.close()
        file = open('vpc_id.txt', 'w+')
        subprocess.run(["jq", ".Vpc.VpcId", "vpc_output.json"], check=True, stdout=file)
        file.close()
        file = open('vpc_id.txt','r+')
        for x in file:
            print(x[1:-2])
            self.vpc_id = x[1:-2]
        file.close()
        subprocess.run(["rm","vpc_output.json","vpc_id.txt","-f"],check=True)

        AWS.CreateSubnet(self)


    def ConfigureInstanceDetails(self):
        print(random.choice(colors) + "----------------------CONFIGURING INSTANCE DETAILS-------------------------")
        self.no_of_instance = input("Enter No of Instances... ")
        choice = int(input("Select Network (VPC).. \n1.Default\n2.Create a new One\nEnter Choice... "))
        if choice == 1:
            self.vpc = "default"
            print(random.choice(colors) + "--------------------------PREPARING DEFAULT VPC--------------------------")
            file_ = open("vpc_output.json",'w+')
            subprocess.run(["aws","ec2","describe-vpcs"],stdout=file_,check=True)
            file_.close()
            file = open("vpc_default_id.txt","w+")
            subprocess.run(["jq", ".Vpcs[0].VpcId", "vpc_output.json"],check=True,stdout=file)
            file.close()
            file = open("vpc_default_id.txt","r+")
            for x in file:
                print(x[1:-2])
                self.vpc_id = x[1:-2]
            file.close()
            subprocess.run(["rm","vpc_output.json","vpc_default_id.txt","-f"],check=True)

            print(random.choice(colors) + "-----------------------PREPARING DEFAULT SUBNET-----------------------")
            file_ = open("subnet_output.json",'w+')
            subprocess.run(["aws","ec2","describe-subnets"],stdout=file_,check=True)
            file_.close()
            file = open("subnet_default_id.txt","w+")
            subprocess.run(["jq", ".Subnets[0].SubnetId", "subnet_output.json"],check=True,stdout=file)
            file.close()
            file = open("subnet_default_id.txt","r+")
            for x in file:
                print(x[1:-2])
                self.cidr_subnet.append(x[1:-2])
            file.close()
            subprocess.run(["rm","subnet_output.json","subnet_default_id.txt","-f"],check=True)

        elif choice == 2:
            AWS.CreateVPC(self)
    

    def CreateEC2Instance(self):
        print(random.choice(colors) + "--------------------------CREATING EC2 INSTANCE--------------------------")
        choice = 1
        while choice == 1:
            AWS.SelectAMIimage(self)
            AWS.InstanceType(self)
            AWS.ConfigureInstanceDetails(self)
            AWS.CreateKeyPair(self)
            AWS.CreateSecurityGroup(self)
            i = 0
            k = 0
            file_ = open('instance_output.json', 'w+')
            self.region = input("Enter the region where you want to launch your Instance... : ")
            print("You have following subnets..... \n")
            for k in range(len(self.cidr_subnet)):
                print(str(k+1) + "--->" +self.cidr_subnet[k])
            ch = int(input("Which subnet from above you want to link with your instance... \nEnter no of subnet... "))
            subprocess.run(["aws", "ec2", "run-instances", "--image-id" ,self.ami_type ,"--count", self.no_of_instance ,"--instance-type" ,self.instance_type ,"--key-name" ,self.key_name , "--region", self.region,"--security-group-ids", self.sg_id ,"--subnet-id" , self.cidr_subnet[ch-1]],check=True,stdout=file_)
 
            file_.close()
            file = open('instance_id.txt', 'w+')
            subprocess.run(["jq", ".Instances[0].InstanceId" , "instance_output.json"],check=True,stdout=file)
            file.close()
            file = open('instance_id.txt', 'r+')
            for x in file:
                print(x[1:-2])
                self.instance_id = x[1:-2]
            self.instance_ids.append(self.instance_id)
            file.close()
            subprocess.run(["rm","instance_output.json","instance_id.txt","-f"],check=True)
            choice = int(input("Do you want to create more instances.......\n1.Yes\n2.No\nEnter Choice... "))
        


    def DescribeEC2Instance(self):
        print(random.choice(colors) + "-------------------------------DESCRIBING INSTANCE-----------------------------")
        print("You have following instances running at current time....")
        i=0
        ch = 0
        for i in range(len(self.instance_ids)):
            print(str(i+1) +"--->"+ self.instance_ids[i])
        print("Do you want to describe above instances or custom one -:\n 1. One of the Above\n 2.Custom one\n")
        choice = int(input("Enter Choice... "))
        if choice == 1:
            ch = int(input("Enter no of the instance you want to describe... "))
            print("You Selected " + str(ch) + "instance. Instance ID-->" , self.instance_ids[ch-1])
            subprocess.run(["aws", "ec2", "describe-instances", "--instance-ids", self.instance_ids[ch-1]],check=True)
        elif choice == 2:
            custom_id = input("Enter Custom Instance Id... ")
            subprocess.run(["aws", "ec2", "describe-instances", "--instance-ids", custom_id],check=True)

    def TerminateEC2Instance(self):
        sample = int(input("Do you want to stop it or terminate it...\n1.Stop\n2.Terminate\nEnter choice... "))
        if sample == 1:
            print(random.choice(colors) + "---------------------------------STOPPING INSTANCE----------------------------")
            print("You have following instances running at current time....")
            i=0
            ch = 0
            for i in range(len(self.instance_ids)):
                print(str(i+1) +"--->"+ self.instance_ids[i])
            print("Do you want to stop above instances or custom one -:\n 1. One of the Above\n2.Custom one\n")
            choice = int(input("Enter Choice... "))
            if choice == 1:
                ch = int(input("Enter no of the instance you want to stop... "))
                print("You Selected " + str(ch) + "instance. Instance ID-->" , self.instance_ids[ch-1])
                subprocess.run(["aws", "ec2", "stop-instances", "--instance-ids", self.instance_ids[ch-1]],check=True)
            elif choice == 2:
                custom_id = input("Enter Custom Instance Id... ")
                subprocess.run(["aws", "ec2", "stop-instances", "--instance-ids", custom_id],check=True)
        elif sample == 2:
            print(random.choice(colors) + "---------------------------------TERMINATING INSTANCE----------------------------")
            print("You have following instances running at current time....")
            i=0
            ch = 0
            for i in range(len(self.instance_ids)):
                print(str(i+1) +"--->"+ self.instance_ids[i])
            print("Do you want to terminate above instances or custom one -:\n 1. One of the Above\n2.Custom one\n")
            choice = int(input("Enter Choice... "))
            if choice == 1:
                ch = int(input("Enter no of the instance you want to terminate... "))
                print("You Selected " + str(ch) + "instance. Instance ID-->" , self.instance_ids[ch-1])
                subprocess.run(["aws", "ec2", "terminate-instances", "--instance-ids", self.instance_ids[ch-1]],check=True)
                self.instance_ids.pop(ch-1)
            elif choice == 2:
                custom_id = input("Enter Custom Instance Id... ")
                subprocess.run(["aws", "ec2", "terminate-instances", "--instance-ids", custom_id],check=True)
        else:
            print("You Selected Nothing")

    def CreateEBSVolume(self):
        print(random.choice(colors) + "-------------------------------CREATING EBS VOLUME--------------------------------")
        choice = int(input("Enter Volume Type... \n1.Default['gp2']\n2.Custom\nEnter Choice.. "))
        volume_type = ""
        if choice == 1:
            volume_type = "gp2"
        elif choice == 2:
            volume_type = input("Enter Custom Volume Type... ")

        size = input("Enter EBS Volume Size... ")
        availability_zone = input("Enter AvailabilityZone... ")
        file_ = open('ebs_output.json', 'w+')
        subprocess.run(["aws" ,"ec2" ,"create-volume" ,"--volume-type", volume_type ,"--size" ,size ,"--availability-zone" ,availability_zone],check=True, stdout=file_)
        file_.close()
        file = open('ebs_id.txt', 'w+')
        subprocess.run(["jq", ".VolumeId", "ebs_output.json"], check=True, stdout=file)
        file.close()
        file = open('ebs_id.txt', 'r+')
        for x in file:
            print(x)
            self.ebs_vol_id = x[1:-2]
        file.close()
        subprocess.run(["rm","ebs_output.json","ebs_id.txt","-f"],check=True)

        print(random.choice(colors) + "---------------------------------ATTACHING EBS VOLUME-----------------------------")
        device_name = input("Enter Device Name for Attached EBS Volume... ")
        device = "/dev/" + device_name
        print("You have following instances running at current time....")
        i = 0
        ch = 0
        for i in range(len(self.instance_ids)):
            print(str(i + 1) + "--->" + self.instance_ids[i])
        print("Do you want to choose above instances or custom one for attaching EBS -:\n 1. One of the Above\n2.Custom one\n")
        choice = int(input("Enter Choice... "))
        if choice == 1:
            ch = int(input("Enter no of the instance you want to attach EBS to it... "))
            print("You Selected " + str(ch) + "instance. Instance ID-->", self.instance_ids[ch - 1])
            subprocess.run(["aws" ,"ec2" ,"attach-volume" ,"--volume-id" ,self.ebs_vol_id ,"--instance-id", self.instance_ids[ch-1], "--device", device],check=True)

        elif choice == 2:
            custom_id = input("Enter Custom Instance Id... ")
            subprocess.run(["aws" ,"ec2" ,"attach-volume" ,"--volume-id" ,self.ebs_vol_id ,"--instance-id", custom_id, "--device", device],check=True)


    def CreateS3Bucket(self):
        print(random.choice(colors) + "--------------------------------CREATING S3 BUCKET---------------------------------")
        self.bucket_name = input("Enter a unique Bucket name... ")
        region = input("Enter Region where you want to create your bucket... ")
        locationConstraint = "LocationConstraint=" + region
        file_ = open('s3_output.json', 'w+')
        subprocess.run(["aws", "s3api" ,"create-bucket" ,"--bucket" ,self.bucket_name ,"--region" ,region ,"--create-bucket-configuration" ,locationConstraint],check=True,stdout=file_)
        file_.close()
        file = open('s3_location.txt', 'w+')
        subprocess.run(["jq", ".Location", "s3_output.json"], check=True, stdout=file)
        file.close()
        file = open('s3_location.txt', 'r+')
        for x in file:
            print(x[1:-2])
            self.s3_location = x[1:-2]
        file.close()
        subprocess.run(["rm","s3_output.json","s3_location.txt","-f"],check=True)
        choice = int(input("Do you Want to add Some Items in your S3 bucket.... \n1.Yes\n2.No"))
        while choice == 1:
            print(random.choice(colors) + "--------------------------------ADDING ITEMS TO S3 BUCKET------------------------------")
            key_directory = input("Enter Key Directory... ")
            body_directory = input("Enter Location of Directory for your Item... ")
            subprocess.run(["aws" , "s3api" , "put-object" , "--bucket" ,  self.bucket_name , "--key" , key_directory , "--body" , body_directory],check=True)
            choice = int(input("Do you Want to add Some More Items in your S3 bucket.... \n1.Yes\n2.No"))

    def CreateCloudFront(self):
        print(random.choice(colors) + "--------------------------------CREATING CLOUDFRONT---------------------------------")
        self.domain_name = input("Enter Domain name for your CloudFront... ")
        self.root_object = input("Enter Default Root Object.. ")
        subprocess.run(["aws", "cloudfront" ,"create-distribution" ,"--origin-domain-name" , f"{self.domain_name}" ,"--default-root-object", self.root_object],check=True)

    def ConnectInstance(self):
        print(random.choice(colors) + "-----------------------------------CONNECTING EC2-INSTANCE----------------------------------")
        print("You have following instances running at current time....\n")
        i=0
        for i in range(len(self.instance_ids)):
            print(str(i+1) +"--->"+ self.instance_ids[i])

        choice = int(input("Do You want to try \n1.These ones \n2.Custom One\nEnter Choice.... "))
        if choice == 1:
            ch = int(input("Select No of Instance... "))
            file_ = open("instance_output.json", "w+")
            subprocess.run(["aws", "ec2", "describe-instances", "--instance-ids", self.instance_ids[ch-1]],check=True,stdout=file_)
            file_.close()
            file = open("instance_ip.txt", "w+")
            subprocess.run(["jq", ".Reservations[0].Instances[0].PrivateIpAddress","instance_output.json"],stdout=file, check=True)
            file.close()
            file = open("instance_ip.txt","r+")
            for x in file:
                instance_ip = x[1:-2]
            file.close()
            subprocess.run(["rm","instance_output.json","instance_ip.txt","-f"],check=True)

        elif choice == 2: 
            instance_ip = input("Enter IP of your Custom Instance... ")

        host_name = instance_ip
        username = "ec2-user"
        private_key_file = input("Enter Path of Private Key for Instance... ")
        shell = spur.SshShell(hostname=host_name, username=username, private_key_file=private_key_file, missing_host_key=spur.ssh.MissingHostKey.accept)
        choice = ""
        cmd = ""
        with shell:
            while choice != "exit":
                choice = input("Enter Command....  ")
                command = choice.split(" ")
                if command.count('cd')>0:
                    while cmd != "exit":
                        cmd = input("Enter Command inside new directory.... ")
                        cmd_command = cmd.split(" ")
                        results = shell.run(cmd_command,cwd=command[1],allow_error=True)
                        print(results.output)
                else:
                    result = shell.run(command,allow_error=True)
                print(result.output)

    def ConnectAnySystem(self):
        print(random.choice(colors) + "-------------------------------------CONNECTING RANDOM SYSTEM---------------------------------")
        host_name = input("Enter IP of the System... ")
        username = input("Enter Username... ")
        password = getpass.getpass("Enter Password...  ")
        shell = spur.SshShell(hostname=host_name, username=username, password=password, missing_host_key=spur.ssh.MissingHostKey.accept)
        choice = ""
        cmd = ""
        with shell:
            while choice != "exit":
                choice = input("Enter Command....  ")
                command = choice.split(" ")
                if command.count('cd')>0:
                    while cmd != "exit":
                        cmd = input("Enter Command inside new directory.... ")
                        cmd_command = cmd.split(" ")
                        results = shell.run(cmd_command,cwd=command[1],allow_error=True)
                        print(results.output)
                else:
                    result = shell.run(command,allow_error=True)
                print(result.output)
                result=""


if __name__ == "__main__":
    a = AWS()
    choice = -1
    while True:
        choice = int(input( random.choice(colors) + "What do you want to do in AWS.....?\n" +random.choice(colors) + "1.Install AWS Cli in your Linux System." + random.choice(colors) +"\n2.Configure AWS for IAM User." + random.choice(colors) + "\n3.Create EC2 Instance." + random.choice(colors)  + "\n4.Describe EC2 Instance\n" + random.choice(colors) + "5.Terminate or Stop EC2 Instance.\n" + random.choice(colors) + "6.Create EBS Storage and Attach it." + random.choice(colors) + "\n7.Create S3 Bucket." + random.choice(colors) + "\n8.Create CloudFront\n" + random.choice(colors) + "9.Connect to EC2 Instance.\n" + random.choice(colors) + "10.Connect to Any System.\n" + random.choice(colors) + "11.Exit." + random.choice(colors) + "\nEnter Choice....." + random.choice(colors)))
        if choice == 1:
            a.installAWSCliV2()
        elif choice == 2:
            a.AWSConfigure()
        elif choice == 3:
            a.CreateEC2Instance()
        elif choice == 4:
            a.DescribeEC2Instance()
        elif choice == 5:
            a.TerminateEC2Instance()
        elif choice == 6:
            a.CreateEBSVolume()
        elif choice == 7:
            a.CreateS3Bucket()
        elif choice == 8:
            a.CreateCloudFront()
        elif choice == 9:
            a.ConnectInstance()
        elif choice == 10:
            a.ConnectAnySystem()
        elif choice == 11:
            break 

