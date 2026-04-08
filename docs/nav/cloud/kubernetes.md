# Kubernetes

Deploy your dotflow pipeline to a Kubernetes cluster.

## Generated files

| File | Description |
|------|-------------|
| `Dockerfile` | Container image |
| `deployment.yaml` | Kubernetes Deployment manifest |
| `service.yaml` | Kubernetes Service manifest |

## Prerequisites

- Docker
- `kubectl`
- A Kubernetes cluster (minikube for local testing)

## Local deploy (minikube)

```bash
# Install minikube (macOS)
brew install minikube

# Start cluster and use its Docker daemon
minikube start
eval $(minikube docker-env)

# Build inside minikube
docker build -t <project_name>:latest .

# Deploy
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Check status
kubectl get pods -l app=<project_name>

# View logs
kubectl logs -l app=<project_name>
```

## Production deploy

Replace `image` in `deployment.yaml` with your container registry URL and change `imagePullPolicy` to `Always`:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Important

- Do not rename `workflow.py` or the `main()` function — the Dockerfile CMD depends on it
- `imagePullPolicy: Never` is for local images only — change to `Always` for production
- Project names with `_` are automatically converted to `-` in Kubernetes resource names
