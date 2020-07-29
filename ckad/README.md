Get all images in all pods:
```sh
$ for ele in `kubectl get po -o jsonpath='{.items[*].spec.containers[*].image}'`; do echo $ele; done
```




### Multi container Pod

 - Create Multi container pod
 - Exec into pod and runn command
 - Update the container image


```sh
$ vim multi-container-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: multic
  name: multic
spec:
  containers:
  - image: nginx
    name: application
    ports:
    - containerPort: 80
  - args:
    - /bin/sh
    - -c
    - echo Proxy container on ubuntu;apt update -y; apt install curl -y;sleep 36000
    image: ubuntu
    name: proxy
  restartPolicy: Never
  ```
  
  ```sh
  $ kubectl apply -f ../jul28/pod.yaml
pod/multic created
  ```

```sh
$ kubectl set image pod/multic application=nginx:1.19
pod/multic image updated
```

```sh
$ kubectl exec -it multic -c proxy -- /bin/bash -c 'curl localhost'
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```


Create a Pod run a command and delete the pod
```sh
$ kubectl run mybusybox --image=ubuntu --restart=Never --rm -it -- /bin/sh -c "echo Hello Kubernetes"
Hello Kubernetes
pod "mybusybox" deleted
```




### Pod Design


Create pod with label 'frontend'
```sh
$ kubectl run test-label1 --image=nginx --labels=application=frontend,tier=production -n jul29 --restart=Never --dry-run -o yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    application: frontend
    tier: production
  name: test-label1
spec:
  containers:
  - image: nginx
    name: test-label1
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}
```

Create another with another label
```sh
$ kubectl run test-label2 --image=nginx --labels=application=backend,tier=production -n jul29 --restart=Never --dry-run -o yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    application: backend
    tier: production
  name: test-label2
spec:
  containers:
  - image: nginx
    name: test-label2
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}
```

```sh
$ kubectl get pods -n jul29 -l application=backend
NAME          READY   STATUS    RESTARTS   AGE
test-label2   1/1     Running   0          23s
$ kubectl get pods -n jul29 -l application=frontend
NAME          READY   STATUS    RESTARTS   AGE
test-label1   1/1     Running   0          6m30s
$ kubectl get pods -n jul29 -l tier=production
NAME          READY   STATUS    RESTARTS   AGE
test-label1   1/1     Running   0          7m2s
test-label2   1/1     Running   0          62s
$ kubectl get pods -n jul29 -l "application in (frontend)"
NAME          READY   STATUS    RESTARTS   AGE
test-label1   1/1     Running   0          30m
$ kubectl get pods -n jul29 -l "tier in (production)"
NAME          READY   STATUS    RESTARTS   AGE
test-label1   1/1     Running   0          30m
test-label2   1/1     Running   0          24m
$ kubectl get pods -n jul29 -l "application in (backend)"
NAME          READY   STATUS    RESTARTS   AGE
test-label2   1/1     Running   0          24m



Show all pod with labels
```sh
$ kubectl get po -n jul29 --show-labels
NAME          READY   STATUS    RESTARTS   AGE   LABELS
test-label1   1/1     Running   0          44m   application=frontend,tier=production
test-label2   1/1     Running   0          38m   application=backend,tier=production
test-label3   1/1     Running   0          7s    application=frontend,tier=development
```

Show all pods with labels with selected labels
```sh
$ kubectl get pods -n jul29 --show-labels -l "application in (backend, frontend)"
NAME          READY   STATUS    RESTARTS   AGE   LABELS
test-label1   1/1     Running   0          41m   application=frontend,tier=production
test-label2   1/1     Running   0          35m   application=backend,tier=production
```


Attaching and dettaching labels-
```sh
$ kubectl label po nginx1 perf- -n jul29
pod/nginx1 labeled

$ kubectl get po --show-labels -n jul29
NAME          READY   STATUS    RESTARTS   AGE     LABELS
nginx1        1/1     Running   0          2m12s   <none>

$ kubectl label po nginx1 perf=black -n jul29
pod/nginx1 labeled

$ kubectl get po --show-labels -n jul29
NAME          READY   STATUS    RESTARTS   AGE     LABELS
nginx1        1/1     Running   0          2m48s   perf=black
```
