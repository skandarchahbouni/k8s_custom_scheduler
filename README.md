
# Kubernetes Custom Scheduler

## Overview
This project implements a **custom Kubernetes scheduler** that dynamically assigns pods to worker nodes based on a random selection strategy. It operates independently of the default Kubernetes scheduler and is deployed within the cluster. 🚀

This project serves as a **template for building custom Kubernetes schedulers** using Python. By default, it binds pods to nodes using **random selection of worker nodes**, but you can modify the logic to implement your own custom scheduling strategy.

## Features
- Watches for pending pods assigned to `my-scheduler`.
- Selects a **random** available worker node.
- Binds the pod to the selected node.
- Uses Kubernetes **RBAC** for security and access control.
- Deployed as a **Kubernetes Deployment** for resilience.

## Project Structure
```
K8S_CUSTOM_SCHEDULER/
│── Dockerfile                  # Builds the scheduler container
│── main.py                     # Scheduler logic
│── requirements.txt            # Python dependencies
│── scheduler-manifests.yml     # Kubernetes RBAC and scheduler deployment
│── cluster-config.yml          # KIND cluster setup
│── test-pod.yml                # Sample pod to test scheduling
│── README.md                   # Project documentation
```

## Prerequisites
- **Docker** (for building and pushing the container image)
- **Kubernetes (KIND)** for local testing
- **kubectl** (CLI tool for Kubernetes management)
- **Python 3.8+**

## Setup & Deployment
### 1️⃣ Create a KIND Cluster
```sh
kind create cluster --config=cluster-config.yml
```
### 2️⃣ Build and Push the Docker Image
```sh
docker build -t skandarchahbouni/my_scheduler .  
docker push skandarchahbouni/my_scheduler:latest
```
_For local testing, load the image directly into KIND:_
```sh
kind load docker-image skandarchahbouni/my_scheduler
```

### 3️⃣ Deploy the Custom Scheduler
```sh
kubectl apply -f scheduler-manifests.yml
```

### 4️⃣ Verify the Deployment
```sh
kubectl get pods -A | grep my-scheduler
```

### 5️⃣ Test the Scheduler
Deploy a test pod that uses `my-scheduler`:
```sh
kubectl apply -f test-pod.yml
kubectl get pods -o wide  # Check scheduling
```

### 6️⃣ View Scheduler Logs
```sh
kubectl logs -f my-scheduler
```

## Demo

Check out the **recorded demo video** to see the custom scheduler in action.

[🎥 Watch the Demo Video](https://drive.google.com/file/d/1RBdda1xv445ZQ29R3-048FOP5OkZLrbk/view?usp=sharing)
