# AWS ECS + EventBridge Schedule

Run your dotflow pipeline on a recurring schedule using ECS Fargate and EventBridge.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image |
| `template.yaml` | CloudFormation template with ECS cluster, task definition, and EventBridge rule |

## Prerequisites

- AWS CLI configured (`aws configure`)
- Docker

## Deploy

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1

# Login, build and push to ECR
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
aws ecr create-repository --repository-name <project_name> --region $REGION
docker build -t <project_name> .
docker tag <project_name>:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/<project_name>:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/<project_name>:latest

# Deploy CloudFormation stack
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name <project_name> \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides SubnetId=<subnet_id> VpcId=<vpc_id> \
  --region $REGION
```

## Important

- The schedule expression is configured during project creation
- The stack creates its own ECS cluster, IAM roles, log group, and security group
- You need to provide `SubnetId` and `VpcId` as parameters
