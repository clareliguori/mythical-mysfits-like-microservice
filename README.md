Demo showing a "likes" microservice for the Mythical Mysfits application

To set up your own Mythical Mysifts application, follow the workshop at [http://aws.amazon.com/build-modern-app](http://aws.amazon.com/build-modern-app).

## Setup

```
export AWS_DEFAULT_REGION=us-east-2

VPC_ID=`aws ec2 describe-vpcs --filters "Name=isDefault, Values=true" --query 'Vpcs[].VpcId' --output text`

SUBNET_IDS=`aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID","Name=default-for-az,Values=true" --query 'Subnets[].SubnetId' --output text | tr "\\t" ","`

aws cloudformation deploy \
    --template-file core.yml \
    --stack-name mythical-mysfits-core-infra \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        VPC=$VPC_ID \
        Subnets=$SUBNET_IDS

aws cloudformation describe-stacks --stack-name mythical-mysfits-core-infra | jq -r '[.Stacks[0].Outputs[] | {key: .OutputKey, value: .OutputValue}] | from_entries'

./script/load-ddb



```

