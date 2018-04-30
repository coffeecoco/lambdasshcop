import boto3
import json
import os
import sys
import uuid

def lambda_handler (event, context):
    ec2 = cboto3.client('ec2')
    instanceid = event('What is your instnace id?')
    userpublicip = event ('What is your public ip? Please use this format: X.X.X.X/32')
    
    try response = ec2.describe_instances(InstanceIds=[instanceid,],DryRun=False,MaxResults=123,): 
        inst = response[0]
        for j in inst 

    SGID = event('security group id')
    response = ec2.describe_security_groups(GroupId=SGID)[0]
