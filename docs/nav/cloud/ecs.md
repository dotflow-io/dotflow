# AWS ECS (Fargate)

Deploy your dotflow pipeline as a Fargate task on Amazon ECS.

## Create project

```bash
dotflow init
# Select cloud: ecs
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform ecs
```

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image |
| `task-definition.json` | ECS task definition for Fargate |

## Prerequisites

- `pip install dotflow[aws]`
- AWS CLI configured (`aws configure`)
- Docker

## Deploy

### Option 1: dotflow deploy

```bash
dotflow deploy --platform ecs --project my_pipeline --region us-east-1
```

This creates: ECR repository, IAM role, CloudWatch log group, ECS cluster, task definition, and pushes the image.

### Option 2: Manual

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
aws ecr create-repository --repository-name my_pipeline --region $REGION
docker build -t my_pipeline .
docker tag my_pipeline:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/my_pipeline:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/my_pipeline:latest

aws logs create-log-group --log-group-name /ecs/my_pipeline --region $REGION
aws ecs register-task-definition --cli-input-json file://task-definition.json --region $REGION
aws ecs create-cluster --cluster-name my_pipeline-cluster --region $REGION

SUBNET=$(aws ec2 describe-subnets --query "Subnets[0].SubnetId" --output text --region $REGION)
aws ecs run-task --cluster my_pipeline-cluster --task-definition my_pipeline --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET],assignPublicIp=ENABLED}" --region $REGION
```

## View logs

```bash
aws logs tail /ecs/my_pipeline --region us-east-1 --since 5m
```

## Important

- Do not rename `workflow.py` or the `main()` function — the Dockerfile CMD depends on it
- Create the CloudWatch log group before running the task
- The `aws_account_id` and `aws_region` must match your actual AWS account
