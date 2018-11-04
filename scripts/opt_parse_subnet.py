#!/usr/bin/env python3
import sys
import boto3
import random
import os
import optparse

def main():
    parser = optparse.OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")
    parser.add_option("-r", "--region-name",
                      action="store",
                      dest="vregion_name",
                      default="us-east-1",
                      type="string",
                      )
    parser.add_option("-v", "--vpc-id",
                      action="store",
                      dest="vpc_id",
                      default=None,
                      )
    options, remainder = parser.parse_args()
    vvpc_id = options.vpc_id
    region_name = options.vregion_name
    #print("VPC ID: ", vvpc_id)
    if vvpc_id is None:
        ec2 = boto3.client('ec2', region_name)
        default_vpc = ec2.describe_vpcs(Filters=[{'Name' : 'isDefault', 'Values' : ['true']}])
        vvpc_id = default_vpc['Vpcs'][0]['VpcId']
        #print("inside VPC ID: ", vvpc_id)
    
    session = boto3.Session(
        region_name = options.vregion_name
    )
    #print(" Region Name: ", region_name )
    # Get EC2 resource
    ec2 = session.resource('ec2')
    # Get VPC resource using Ec2 resource by supplying VPC ID
    vpc = ec2.Vpc(vvpc_id)

    # Check whether VPC has subnets and display them accordingly
    subnets = list(vpc.subnets.all())
    print(random.choice(subnets).id)
    if len(subnets) == 0:
        print("There is no subnet in this VPC!")

if __name__ == "__main__":
    main()
