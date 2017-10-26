#!/usr/bin/env python3

import boto3
import time
import subprocess
import sys

ec2 = boto3.resource('ec2')
s3 = boto3.resource("s3")

#create an instance
def create_instance():


    instance = ec2.create_instances(
        ImageId='ami-acd005d5',
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=['sg-e8c22993'],
        KeyName='paddykeypair',
        UserData='''#!bin/bash
            yum -y update
            yum -y install nginx
            yum -y install python35
            service nginx start
            chkconfig nginx on
            touch /home/ec2-user/testfile''',
        InstanceType='t2.micro')

    print()
    print("CREATING INSTANCE")
    print("-------------------")
    time.sleep(1)
    print("An instance with ID: ", instance[0].id, " has been created.")
    print()
    print("RETRIEVING PUBLIC IP ADDRESS")
    print("-------------------")
    time.sleep(5)
    instance = instance[0]
    instance.reload()
    print("Public IP address: ", instance.public_ip_address)
    print()

    return instance


#check to see if ssh will work on instance
def ssh_check(instance):


    #create a public ip variable for instance
    pub_ip_inst = instance.public_ip_address

    #ssh check command
    print("CHECKING SSH ACCESS ON INSTANCE...")
    cmd_ssh_check = "ssh -o StrictHostKeyChecking=no -i ~/dev-ops/paddykeypair.pem ec2-user@" + pub_ip_inst + " 'pwd'"
    time.sleep(40)
    print("-------------------")
    instance.reload()
    (status, output) = subprocess.getstatusoutput(cmd_ssh_check)
    print("output: " + output)
    print("status: ", status)
    if status == 0:
        print("ssh test passed")
    else:
        print("ssh test failed")

    return pub_ip_inst


# copy check_webserver.py to the instance
def securecopy_check_webserver(pub_ip_inst):
    time.sleep(2)
    print()
    print("COPYING CHECK_WEBSERVER.PY TO INSTANCE")
    print("-------------------")
    time.sleep(1)
    cmd_scp = "scp -i ~/dev-ops/paddykeypair.pem check_webserver.py ec2-user@" + pub_ip_inst + ":."
    # carrying out secure copy command
    (status, output) = subprocess.getstatusoutput(cmd_scp)
    print("output: " + output)
    print("status: ", status)
    # check if check_webserver was copied
    if (status == 0):
        print("check_webserver successfully copied")
    else:
        print("check_webserver not copied")


# execute the check_webserver
def execute_check_webserver(pub_ip_inst):
    time.sleep(2)
    print()
    print("MAKING CHECK_WEBSERVER.PY EXECUTABLE")
    print("-------------------")
    time.sleep(1)
    # make the check_webserver.py file executable before its run
    make_executable = "ssh -i ~/dev-ops/paddykeypair.pem ec2-user@" + pub_ip_inst + " 'chmod +x check_webserver.py'"
    (status, output) = subprocess.getstatusoutput(make_executable)
    print("output: " + output)
    print("status: ", status)
    # let user know if check_webserver is executable or not
    if(status == 0):
        print("check_webserver is executable")
        time.sleep(2)

        print()
        print("EXECUTING CHECK_WEBSERVER.PY")
        print("-------------------")
        time.sleep(1)
        # after informing user that it's executable, run the file
        exe_check_webserver = "ssh -i ~/dev-ops/paddykeypair.pem ec2-user@" + pub_ip_inst + " './check_webserver.py'"
        print("command to run: ", exe_check_webserver)
        (status, output) = subprocess.getstatusoutput(exe_check_webserver)
        # print the output and status of the check_webserver file when run
        print("output: " + output)
        print("status: ", status)
        # let user know whether the file execution was successful or not
        if (status == 0):
            print("execute_check_webserver successful")
        else:
            print("execute_check_webserver failed")
    else:
        print("check_webserver is not executable")


# creating a new bucket
def create_bucket():
    time.sleep(2)
    print()
    print("CREATING A BUCKET")
    print("-------------------")
    time.sleep(1)
    # get bucket name input from user
    bucket_name = input("Please Enter Bucket name: ")
    try:
        # create bucket with location in Ireland
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        # if bucket successfully created then print message for user
        print("creating bucket successful")
        print(response)
    # if there is an error creating a bucket, print message for user
    except Exception as error:
        print(error)


def main():
    instance = create_instance()
    pub_ip_inst = ssh_check(instance)
    securecopy_check_webserver(pub_ip_inst)
    execute_check_webserver(pub_ip_inst)
    create_bucket()


if __name__ == '__main__':
    main()