import boto3
import requests

def lambda_handler(event, context):
	# Get List of Cloudfront IPs
	get_ips = requests.get('http://d7uri8nf7uskq.cloudfront.net/tools/list-cloudfront-ips')
	cloudfront_ip = get_ips.json()

	ec2cl = boto3.client('ec2')
	ec2r = boto3.resource('ec2')

	# Get Security Group ID
	get_sg = ec2cl.describe_security_groups(
    	Filters=[
        	{
            	'Name': 'tag-value',
            	'Values': [
                	'autoupdate',
            	]
        	},
        	{
        		'Name': 'tag-key',
        		'Values': [
        			'cloudfront',
        		]
        	},
    	],
	)

	sg_ids = []
	for ids in get_sg['SecurityGroups']:
		sg_ids.append(ids['GroupId'])

	# Setup variables to create rules
	http_params = {
		'FromPort': 80,
		'IpRanges': [],
		'ToPort': 80,
		'IpProtocol': 'tcp',
	}

	https_params = {
		'FromPort': 443,
		'IpRanges': [],
		'ToPort': 443,
		'IpProtocol': 'tcp',
	}

	authorize_http_ips = http_params.copy()
	authorize_https_ips = https_params.copy()

	# Populate IPs into the parameter variable
	for ip in cloudfront_ip['CLOUDFRONT_GLOBAL_IP_LIST']:
		authorize_http_ips['IpRanges'].append({'CidrIp': ip})
		authorize_https_ips['IpRanges'].append({'CidrIp': ip})

	# Drop existing rules
	for sgid in sg_ids:
		sg = ec2r.SecurityGroup(sgid)
		sg.revoke_ingress(IpPermissions=sg.ip_permissions)

	# Create Rules
	for sgid in sg_ids:
		sg = ec2r.SecurityGroup(sgid)
		sg.authorize_ingress(IpPermissions=[authorize_http_ips,authorize_https_ips])


