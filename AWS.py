import subprocess
import json

class AWS():
    def __init__(self, ami_type="",instance_type="",no_of_instance=1,vpc="", cidr="10.0.0.0/16",vpc_id="",igw="",route_table_id="",cidr_subnet=[],key_name="",sg_id="",ebs_vol_id="", instance_id="",s3_location=""):
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
        sg_output = subprocess.run(["aws" ,"ec2" ,"create-security-group" ,"--group-name" ,group_name ,"--description", description ,"--vpc-id", self.vpc_id],check=True)
        data = json.loads(sg_output)
        self.sg_id = data["GroupId"]
        protocol = input("Enter Protocol for your Security Group... ")
        port = input("Enter Port No for your Security Group... ")
        cidr = input("Enter CIDR block for your Security Group... ")
        print("-----------------------------AUTHORIZING SECURITY GROUP---------------------------")
        subprocess.run(["aws","ec2","authorize-security-group-ingress" ,"--group-id",self.sg_id ,"--protocol", protocol, "--port" , port, "--cidr" , cidr],check=True)


    def CreateKeyPair(self):
        print("--------------------------CREATING KEY PAIR------------------------------")
        self.key_name = input("Enter KeyName for Keypair... ")
        key_filename = self.key_name + ".pem"
        subprocess.run(["aws", "ec2" ,"create-key-pair" ,"--key-name" ,self.key_name "--query" ,"'KeyMaterial'" ,"--output" ,"text" ,">" , key_filename],check=True)
        print("--------------------------Changing KEY-FILE PERMISSIONS------------------------")
        subprocess.run(["sudo", "chmod", "400", key_filename],check=True)

    def CreateRouteTable(self):
        print("---------------------------CREATING ROUTE TABLE-----------------------------")
        route_table_output = subprocess.run(["aws","ec2","create-route-table","--vpc-id",self.vpc_id], check=True)
        data = json.loads(route_table_output)
        self.route_table_id = data["RouteTableId"]
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
        igw_output = subprocess.run(["aws","ec2","create-internet-gateway"],check=True)
        data = json.loads(igw_output)
        self.igw = data['InternetGatewayId']

        print("----------------------------ATTACHING INTERNET GATEWAY-----------------------")
        subprocess.run(["aws", "ec2", "attach-internet-gateway", "--vpc-id", self.vpc_id, "--internet-gateway-id", self.igw],check=True)

    def CreateSubnet(self):
        print("----------------------------CREATING SUBNET----------------------------------")
        choice = 1
        self.cidr_subnet = []
        i=0
        while choice == 1:
            self.cidr_subnet[i] = input("Enter cidr block value.. ")
            subprocess.run(["aws","ec2","create-subnet","--vpc-id",self.vpc_id, "--cidr-block",self.cidr_subnet[i]], check=True)
            choice = int(input("Do you want to create more Subnets..?\n1.Yes\n2.No\nEnter Choice.. "))
            if choice == 1:
                i=i+1
            elif choice:
                break        

    def CreateVPC(self):
        print("----------------------CREATING VIRTUAL PRIVATE CLOUD-----------------------")
        self.cidr = input("Enter CIDR Block.... ")
        vpc_output = subprocess.run(["aws", "ec2","create-vpc", "--cidr-block",self.cidr], check=True)
        data = json.loads(vpc_output)
        self.vpc_id = data['VpcId']


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
        AWS.SelectAMIimage(self)
        AWS.InstanceType(self)
        AWS.ConfigureInstanceDetails(self)

    def DescribeEC2Instance(self):
        print("-------------------------------DESCRIBING INSTANCE-----------------------------")
        pass

    def TerminateEC2Instance(self):
        print("-------------------------------TERMINATING INSTANCE------------------------------")
        pass

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
        subprocess.run(["aws" ,"ec2" ,"attach-volume" ,"--volume-id" ,self.ebs_vol_id ,"--instance-id", self.instance_id, "--device", device),check=True]
    
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
    a.installAWSCliV2()