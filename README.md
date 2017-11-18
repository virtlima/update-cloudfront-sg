# update-cloudfront-sg
This Lambda code and SAM template together update security groups when cloudfront IPs are updated.

### Pre-requisites
- Existing Security Groups with Rules that allows only Cloudfront IPs on http and https
- Security Groups are Tagged with Key: cloudfront and Value: autoupdate


### The SAM template creates the following resources:
- 1 Lambda Function 
- 1 IAM Role with 1 Managed Policy and 1 Custom Policy
- 1 SNS Event that triggers the Lambda function when Amazon IP Ranges are updated


### High level flow
Once set up, this would work as follows:

- Amazon updates IP Ranges 
- Update message sent to subscribed SNS topic and triggers the Lambda function 
- Lambda drops current rules in tagged security groups, re-populates with latest IP ranges
