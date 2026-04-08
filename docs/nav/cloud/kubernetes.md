# Kubernetes

Deploy your dotflow pipeline to a Kubernetes cluster.

## Create project

```bash
dotflow init
# Select cloud: kubernetes
```

Or generate files for an existing project:

```bash
dotflow cloud generate --platform kubernetes
```

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

## Deploy (local with minikube)

```bash
brew install minikube
minikube start
eval $(minikube docker-env)

docker build -t my_pipeline:latest .

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Deploy (production)

Replace `image` in `deployment.yaml` with your container registry URL and change `imagePullPolicy` to `Always`:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## View logs

```bash
kubectl logs -l app=my_pipeline
```

## Important

- Do not rename `workflow.py` or the `main()` function — the Dockerfile CMD depends on it
- `imagePullPolicy: Never` is for local images only — change to `Always` for production
- Project names with `_` are automatically converted to `-` in Kubernetes resource names
