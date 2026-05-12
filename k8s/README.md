# Kubernetes Deployment Guide

## Prerequisites
- A running Kubernetes cluster (local: minikube / kind; cloud: GKE, EKS, AKS)
- kubectl configured
- Nginx Ingress Controller installed
- Docker images built and pushed to a registry

## Quick Deploy

```bash
# 1. Build and push images
docker build -t your-dockerhub-username/finplatform-backend:latest ./backend
docker build -t your-dockerhub-username/finplatform-frontend:latest ./frontend
docker push your-dockerhub-username/finplatform-backend:latest
docker push your-dockerhub-username/finplatform-frontend:latest

# 2. Edit k8s/secrets.yaml with real API keys (never commit real values)

# 3. Apply all manifests in order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/database/
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/

# 4. Verify
kubectl get all -n finplatform
```

## Useful Commands
```bash
kubectl logs deployment/backend  -n finplatform   # Backend logs
kubectl logs deployment/frontend -n finplatform   # Frontend logs
kubectl exec -it deployment/backend -n finplatform -- bash  # Shell in
kubectl rollout restart deployment/backend  -n finplatform  # Redeploy
kubectl rollout restart deployment/frontend -n finplatform
```
