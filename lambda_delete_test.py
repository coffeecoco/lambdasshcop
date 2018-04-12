#this is some python2.7 code written by tope oyenuga (@nugii__) to revoke SSH and all ports ingress on AWS seucrity groups in a region. This is meant to be run in aws lambda

import boto3
import json
import sys
import copy
import urllib2

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.describe_security_groups(
        Filters=[
            {'Name': 'ip-permission.from-port','Values': ['22','0',]},{'Name': 'ip-permission.to-port','Values': ['22','65535',]},
            ]
    ) #filtering for only security groups that have port 22 ingress opened or all ports opened  
    

    for secgroup in response['SecurityGroups']:     #make secgroup = to json data after SecurityGroups in response
        SGIDs = ''                                  #initialize empty variable 
        for secgroupids in secgroup['GroupId']:     #loop to search for GroupId string within secgroupids 
            SGIDs = SGIDs + secgroupids             #cocotenation to make up for printing character by character 
        print SGIDs

        #describing my selected security group
        selected_sg = ec2.describe_security_groups(GroupIds=[SGIDs])    

        #select data after SecurityGroups
        selected_sg_data = selected_sg['SecurityGroups'][0]
        
        #store IpPermissions into permission
        permission = selected_sg_data['IpPermissions']      #selecting dictionary of IpPermissions
        for x in permission:
            if x['FromPort'] != '22':           #match all dictionaries in permission with port 22 
                permission.remove(x)            #delete said dictionary in permission 
                print x
                break
        
        #revoke IpPermissions of any SSH port 22 ingress for selected securtiy group
        ec2.revoke_security_group_ingress(GroupId=SGIDs,IpPermissions=permission,)

        for x in permission:
            if x['FromPort'] != '0' and x['ToPort'] != '65535':         #match all dictionaries in permission with all ports open 
                permission.remove(x)                                    #selete said dictionary in permission 
                break

        ec2.revoke_security_group_ingress(GroupId=SGIDs,IpPermissions=permission,)