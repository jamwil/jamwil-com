+++
title = "Running a local Kubernetes cluster with Kind: A step-by-step guide"
date = "2023-06-20T02:36:00Z"
[taxonomies]
tags = ["docker", "kubernetes", "kind", "local-development", "tooling"]
categories = ["Technology"]
+++

It has happened. I thought I could avoid it, but here we are. As if getting your
program to run on one computer wasn't hard enough, now we have to run it on
multiple computers at the same time? They have played us for absolute fools.

Anyway, assuming we have some shared experience with Docker, let's introduce
some terminology:

- A **Pod** is the smallest deployable unit in Kubernetes, often a single
  instance of an application. As I understand it, a pod is the logical
  equivalent of a container.
- **Nodes** are the machines that host these pods. More nodes allow for more
  redundancy.
- A **Cluster** is a set of nodes with the same job. A cluster can run multiple
  nodes, and a node can run multiple pods, and a pod typically consists of
  between two and fifteen orca whales.
- A **Service** is an abstraction which provides a single network entry point to
  distribute traffic across the cluster.

For local development I am using [Kind](https://kind.sigs.k8s.io), a tool which
allows you to run Kubernetes clusters in Docker containers. It is a lightweight
way to run docker containers inside kubernetes inside a docker container (pause
for effect).

The command to create a cluster is: `kind create cluster`

To deploy the application, it needs to be packaged as a Docker image. After
creating the Dockerfile, the image is built and loaded into the Kind cluster
with the following commands:

`docker build -t my-image-name .`

`kind load docker-image my-image-name`

I should note that in addition to Kind, there is a tool called minikube which is
similar, though it requires you to set up a container registry.

The next step is creating a deployment and a service for the application by
creating kubernetes manifest files in your project directory. The simplest
possible configuration is something like so:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-image-name-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-image-name
  template:
    metadata:
      labels:
        app: my-image-name
    spec:
      containers:
        - name: my-image-name
          image: my-image-name
          imagePullPolicy: Never # Use for local image
          ports:
            - containerPort: 8000 # Use the port your application runs on
```

Note that the `imagePullPolicy` is set to `Never` because we are using a local
image with the implied tag `latest`. Specifying a specific tag should make this
unnecessary, otherwise the default behaviour is to try to pull the image from
Docker Hub, which will fail each time (or worse, deploy something unexpected).

In addition to matching the exposed port of the container, your application
should be configured to bind to any incoming address (0.0.0.0), not just
localhost.

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-image-name-service
spec:
  type: NodePort
  ports:
    - port: 8000
      nodePort: 30080
  selector:
    app: my-image-name
```

With these files in place, we can create the deployment and service respectively
using `kubectl apply -f <file-name>` for each. They can be verified using:
`kubectl get deployments` and `kubectl get services`.

If there are any issues, logs can be checked using: `kubectl logs <pod-name>`,
and the pod name can be found using `kubectl get pods`.

Remember to specify environment variables in the `deployment.yaml` file under
`env` in the `containers` specification if your application requires them.

If you're running docker inside a linux virtual machine, port 30080 should
already be exposed. If you're running using Docker Desktop, there's one more
step which requires forwarding a local port to the service port. This can be
done using:

`kubectl port-forward service/my-image-name-service 30080:8000`

This will map the service to `localhost:30080` on your local machine. Launch it
in tmux or append the command with an ampersand as it will block the terminal
otherwise.

Fin. Now deploy to prod on a Friday afternoon and you're done!

<!-- more -->
