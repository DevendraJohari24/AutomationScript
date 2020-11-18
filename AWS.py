import subprocess
import json
import os

class AWS():
    def __init__(self, ami_type="",instance_type="",no_of_instance=1,vpc="", cidr="10.0.0.0/16",vpc_id="",igw="",route_table_id="",cidr_subnet=[],key_name="",sg_id="",ebs_vol_id="", instance_id="",s3_location="",instance_ids=[]):
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
        

    def installAWSCliV2(self):
        print("----------------------------INSTALLING AWS-------------------------------")
        try:
            subprocess.run(["aws", "--version"], check=True)
            print("AWS already configured in your system......")
        except:
            downloading_link = "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
            folder_name = "awscliv2.zip"
            subprocess.run(["curl", downloading_link, "-o", folder_name],check=True)
            subprocess.run(["unzip", "awscliv2.zip"],check=True)
            subprocess.run(["./aws/install"], check=True)
            print("-------------------SUCCESSFULLY INSTALLED----------------------------")

    def installJSON(self):
        print("----------------------------INSTALLING JQ--------------------------------")
        try:
            subprocess.run(["jq","--help"],check=True)
            print("You already have jq installed in your system.....")
        except:
            subprocess.run(["sudo", "apt-get","install","jq"], check=True)
            print("Jq installed successfully in your system.....")
    
    def AWSConfigure(self):
        print("--------------------------CONFIGURING AWS--------------------------------")
        print("Enter Credientials........")
        try:
            subprocess.run(["aws", "configure"], check=True)
        except:
            print("-------------AWS NOT CONFIGURED IN YOUR SYSTEM----------------")
            AWS.installAWSCliV2(self)
            subprocess.run(["aws", "configure"], check=True)
        print("-------------------------AWS CONFIGURED SUCCESSFULLY---------------------")

    def SelectAMIimage(self):
        print("------------------------SELECTING AMI IMAGE-------------------------")
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
        print("---------------------------SELECTING INSTANCE TYPE------------------------")
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
        print("----------------------------CREATING SECURITY GROUP--------------------------")
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
        protocol = input("Enter Protocol for your Security Group... ")
        port = input("Enter Port No for your Security Group... ")
        cidr = input("Enter CIDR block for your Security Group... ")
        print("-----------------------------AUTHORIZING SECURITY GROUP---------------------------")
        subprocess.run(["aws","ec2","authorize-security-group-ingress" ,"--group-id",self.sg_id ,"--protocol", protocol, "--port" , port, "--cidr" , cidr],check=True)


    def CreateKeyPair(self):
        print("--------------------------CREATING KEY PAIR------------------------------")
        self.key_name = input("Enter KeyName for Keypair... ")
        file_ = open(f'{self.key_name}.pem', 'w+')
        subprocess.run(["aws", "ec2" ,"create-key-pair" ,"--key-name" ,self.key_name , "--query" ,"KeyMaterial" ,"--output" ,"text" ],check=True, stdout=file_)
        file_.close()
        print("--------------------------Changing KEY-FILE PERMISSIONS------------------------")
        key_filename = self.key_name + ".pem"
        subprocess.run(["sudo", "chmod", "400", key_filename],check=True)

    def CreateRouteTable(self):
        print("---------------------------CREATING ROUTE TABLE-----------------------------")
        file_ = open('route_table.json', 'w+')
        subprocess.run(["aws","ec2","create-route-table","--vpc-id",self.vpc_id], check=True, stdout=file_)
        file_.close()
        file = open('route_table_id.txt', 'w+')
        subprocess.run(["jq", ".RouteTable[0].RouteTableId", "route_table.json"], check=True, stdout=file)
        file.close()
        file = open('route_table_id.txt', 'r+')
        for x in file:
            print(x[1:-2])
            self.route_table_id = x[1:-2]
        file.close()
        print("---------------------------ATTACHING ROUTE TABLE-----------------------------")
        destination_cidr_block=""
        choice = int(input("Enter Destination CIDR Block....\nDo you want to make it by \n1.Default[0.0.0.0/0]\n2.Custom\nEnter Choice... "))
        if choice == 1:
            destination_cidr_block = "0.0.0.0/0"
        elif choice == 2:
            destination_cidr_block = input("Enter Custom Destination CIDR Block.. ")
        subprocess.run(["aws","ec2","create-route","--route-table-id",self.route_table_id,"--destination-cidr-block",destination_cidr_block,"--gateway-id", self.igw],check=True)
        print("--------------------------CHOOSE SUBNET FOR ROUTE TABLE------------------------")
        print("You have created following Subnets -: ")
        for i in range(len(self.cidr_subnet)):
            print((i+1) + "--->" + self.cidr_subnet[i])
        while True:
            print("---------------------------ASSOCIATING SELECTED SUBNET TO ROUTE TABLE----------------------------")
            ch = int(input("Choose one of the above subnets... "))
            subprocess.run(["aws" ,"ec2", "associate-route-table" ,"--subnet-id" ,self.cidr_subnet[ch] ,"--route-table-id" ,self.route_table_id],check=True)
            choice = int(input("Do you want to associate more subnets..\n1.Yes\n2.No\nEnter Choice.. "))

    def CreateInternetGateway(self):
        print("----------------------------CREATING INTERNET GATEWAY------------------------")
        file_ = open('igw.json', 'w+')
        subprocess.run(["aws","ec2","create-internet-gateway"],check=True,stdout=file_)
        file_.close()
        file = open('igw_id.txt', 'w+')
        subprocess.run(["jq", ".InternetGateway[0].InternetGatewayId", "igw.json"], check=True, stdout=file)
        file.close()
        file = open('igw_id.txt', 'r+')
        for x in file:
            print(x[1:-2])
            self.igw = x[1:-2]
        file.close()
        print("----------------------------ATTACHING INTERNET GATEWAY-----------------------")
        subprocess.run(["aws", "ec2", "attach-internet-gateway", "--vpc-id", self.vpc_id, "--internet-gateway-id", self.igw],check=True)
        AWS.CreateRouteTable(self)


    def CreateSubnet(self):
        print("----------------------------CREATING SUBNET----------------------------------")
        choice = 1
        self.cidr_subnet = []
        i=0
        while choice == 1:
            cidr_subnet = input("Enter cidr block value.. ")
            file_ = open('subnet.json','w+')
            subprocess.run(["aws","ec2","create-subnet","--vpc-id",self.vpc_id, "--cidr-block",cidr_subnet], check=True,stdout=file_)
            file_.close()
            file = open('subnet_id.txt', 'w+')
            subprocess.run(["jq", f".[{i}].ID", "subnet.json"], check=True, stdout=file)
            file.close()
            file = open('subnet_id.txt','r+')
            for x in file:
                print(x[1:-2])
                self.cidr_subnet[i] = x[1:-2]
            file.close()
            choice = int(input("Do you want to create more Subnets..?\n1.Yes\n2.No\nEnter Choice.. "))
            if choice == 1:
                i=i+1
            elif choice == 2:
                break   

        AWS.CreateInternetGateway(self)     

    def CreateVPC(self):
        print("----------------------CREATING VIRTUAL PRIVATE CLOUD-----------------------")
        self.cidr = input("Enter CIDR Block.... ")
        file_ = open('vpc_output.json', 'w+')
        subprocess.run(["aws", "ec2","create-vpc", "--cidr-block",self.cidr], check=True,stdout=file_)
        file_.close()
        file = open('vpc_id.txt', 'w+')
        subprocess.run(["jq", ".Vpc[0].VpcId", "vpc_output.json"], check=True, stdout=file)
        file.close()
        file = open('vpc_id.txt','r+')
        for x in file:
            print(x[1:-2])
            self.vpc_id = x[1:-2]

        file.close()
        AWS.CreateSubnet(self)


    def ConfigureInstanceDetails(self):
        print("----------------------CONFIGURING INSTANCE DETAILS-------------------------")
        self.no_of_instance = input("Enter No of Instances... ")
        choice = int(input("Select Network (VPC).. \n1.Default\n2.Create a new One\nEnter Choice... "))
        if choice == 1:
            self.vpc = "default"
        elif choice == 2:
            AWS.CreateVPC(self)
    

    def CreateEC2Instance(self):
        print("--------------------------CREATING EC2 INSTANCE--------------------------")
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
            if len(self.cidr_subnet) != 0:
                print("You have following subnets..... \n")
                for k in range(len(self.cidr_subnet)):
                    print(str(k+1) + "--->" +self.cidr_subnet[k])
                ch = int(input("Which subnet from above you want to link with your instance... \nEnter no of subnet... "))
                subprocess.run(["aws", "ec2", "run-instances", "--image-id" ,self.ami_type ,"--count", self.no_of_instance ,"--instance-type" ,self.instance_type ,"--key-name" ,self.key_name ,"--security-group-ids", self.sg_id ,"--subnet-id" , self.cidr_subnet[ch-1],">","instance_output.json"],check=True,stdout=file_)
            else:
                subprocess.run(["aws", "ec2", "run-instances", "--image-id" ,self.ami_type ,"--count", self.no_of_instance ,"--instance-type" ,self.instance_type ,"--key-name" ,self.key_name ,"--security-group-ids", self.sg_id ],check=True,stdout=file_)
 
            file_.close()
            file = open('instance_id.txt', 'w+')
            subprocess.run(["jq", ".Instances[0].InstanceId" , "instance_output.json"],check=True,stdout=file)
            file.close()
            file = open('instance_id.txt', 'r+')
            for x in file:
                print(x[1:-2])
                self.instance_id = x[1:-2]
            self.instance_ids[i] = self.instance_id
            file.close()
            choice = int(input("Do you want to create more instances.......\n1.Yes\n2.No\nEnter Choice... "))   
            if choice == 1:
                i = i+1
                continue
            elif choice == 2:
                break


    def DescribeEC2Instance(self):
        print("-------------------------------DESCRIBING INSTANCE-----------------------------")
        print("You have following instances running at current time....")
        i=0
        ch = 0
        for i in range(len(self.instance_ids)):
            print(str(i+1) +"--->"+ self.instance_ids[i])
        print("Do you want to describe above instances or custom one -:\n 1. One of the Above\n2.Custom one\n")
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
            print("---------------------------------STOPPING INSTANCE----------------------------")
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
            print("---------------------------------STOPPING INSTANCE----------------------------")
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
            elif choice == 2:
                custom_id = input("Enter Custom Instance Id... ")
                subprocess.run(["aws", "ec2", "terminate-instances", "--instance-ids", custom_id],check=True)

    def CreateEBSVolume(self):
        print("-------------------------------CREATING EBS VOLUME--------------------------------")
        choice = int(input("Enter Volume Type... \n1.Default['gp2']\n2.Custom\nEnter Choice.. "))
        volume_type = ""
        if choice == 1:
            volume_type = "gp2"
        elif choice == 2:
            volume_type = input("Enter Custom Volume Type... ")

        size = input("Enter EBS Volume Size... ")
        availability_zone = input("Enter AvailabilityZone... ")
        ebs_output = subprocess.run(["aws" ,"ec2" ,"create-volume" ,"--volume-type", volume_type ,"--size" ,size ,"--availability-zone" ,availability_zone],check=True)
        data = json.loads(ebs_output)
        self.ebs_vol_id = data["VolumeId"]

        print("---------------------------------ATTACHING EBS VOLUME-----------------------------")
        device_name = input("Enter Device Name for Attached EBS Volume... ")
        device = "/dev/" + device_name
        subprocess.run(["aws" ,"ec2" ,"attach-volume" ,"--volume-id" ,self.ebs_vol_id ,"--instance-id", self.instance_id, "--device", device],check=True)
    
    def CreateS3Bucket(self):
        print("--------------------------------CREATING S3 BUCKET---------------------------------")
        bucket_name = input("Enter a unique Bucket name... ")
        region = input("Enter Region where you want to create your bucket... ")
        locationConstraint = "LocationConstraint="+ region
        s3_bucket_output = subprocess.run(["aws", "s3api" ,"create-bucket" ,"--bucket" ,bucket_name ,"--region" ,region ,"--create-bucket-configuration" ,locationConstraint],check=True)
        data = json.loads(s3_bucket_output)
        self.s3_location = data['Location']


    def LaunchWebServer(self):
        print("--------------------------------LAUNCHING WEBSERVER---------------------------------")
        pass

    def LaunchDatabaseServer(self):
        print("-------------------------------LAUNCHING DATABASE SERVER-------------------------")
        pass

if __name__ == "__main__":
    a = AWS()
    a.CreateEC2Instance()