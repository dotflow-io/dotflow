# AWS ECS + EventBridge Schedule

Run your dotflow pipeline on a recurring schedule using ECS Fargate and EventBridge.

## Create project

```bash
dotflow init
# Select cloud: ecs-scheduled
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform ecs-scheduled
```

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

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
aws ecr create-repository --repository-name my_pipeline --region $REGION
docker build -t my_pipeline .
docker tag my_pipeline:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/my_pipeline:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/my_pipeline:latest

aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my_pipeline \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides SubnetId=<subnet_id> VpcId=<vpc_id> \
  --region $REGION
```

## Important

- Use standard cron format (e.g. `0 */6 * * *`). Dotflow converts to AWS EventBridge format automatically
- The stack creates its own ECS cluster, IAM roles, log group, and security group
- You need to provide `SubnetId` and `VpcId` as parameters
