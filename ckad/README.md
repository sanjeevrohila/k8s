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
$ kubectl get po --show-labels -n jul29
nginx1        1/1     Running   0          84s     perf=black


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


### Taints and Tolerations

| Taint Effect | Specification | additional Info|
| ------------ | ------------- | ---------------|
| NoSchedule | No pod scheduling allowed without tolrence | No impact on existing pods |
| PreferNoSchedule | Tries not to allow pod scheduling | No impact on existing pods |
| NOExecute | No pod scheduling allowed without tolrence | Evicts existing pods |

```sh
kubectl taint node <node name> key=value:<taint_effect>
```

Taint a Node
```sh
#Taint a node
$ kubectl taint node host-1 application=mebuy:NoSchedule

# Check the taint on node
$ kubectl describe node host-1 | grep Taint
Taints:             application=mebuy:NoSchedule

#Schedule a pod
$ cat taint-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: taint-pod
  name: taint-pod
spec:
  containers:
  - image: nginx
    name: taint-pod-container
  tolerations:
  - key: "application"
    operator: "Equal"
    value: "mebuy"
    effect: "NoSchedule"
  dnsPolicy: ClusterFirst
  restartPolicy: Never

#Check the node affinity of pod
$ kubectl get po taint-pod -n jul29 -o jsonpath='{.spec.nodeName}{"\n"}'
host-1
```



### Node Labeling

```sh
# Labeling host-2 as its hardware is hyperthreading enabled
$ kubectl label node host-2 hardware=hyperthreaded
node/host-2 labeled

#Check the labels
$ kubectl get nodes --show-labels
NAME         STATUS   ROLES    AGE   VERSION   LABELS
host-1       Ready    <none>   71d   v1.18.2   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=host-1,kubernetes.io/os=linux
host-2       Ready    <none>   71d   v1.18.2   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,hardware=hyperthreaded,kubernetes.io/arch=amd64,kubernetes.io/hostname=host-2,kubernetes.io/os=linux
ubuntu1604   Ready    master   71d   v1.18.2   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=ubuntu1604,kubernetes.io/os=linux,node-role.kubernetes.io/master=
``` 


### Create a pod with node selector with label
```sh
#Create basic pod
$ kubectl run node-label-pod --image=nginx --restart=Never --dry-run -o yaml -n jul29

#Add aditional field to select Node
#Edit as node label pod
$vim node-label-pod.yaml
$ cat node-label-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: node-label-pod
  name: node-label-pod
spec:
  containers:
  - image: nginx
    name: node-label-pod
    resources: {}
  nodeSelector:
    hardware:  hyperthreaded #label to select
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}

#Create pod
$ kubectl apply -f node-label-pod.yaml -n jul29
pod/node-label-pod created

#check pod affinity
$ kubectl get pod node-label-pod -n jul29 -o jsonpath='{.spec.nodeName}{"\n"}'
host-2
$ kubectl get pod node-label-pod -n jul29 -o jsonpath='{.spec.nodeSelector}{"\n"}'
map[hardware:hyperthreaded]


#Impact of un-labeling
$ kubectl label node host-2 hardware-
node/host-2 labeled

$ kubectl get nodes --show-labels
NAME         STATUS   ROLES    AGE   VERSION   LABELS
host-1       Ready    <none>   71d   v1.18.2   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=host-1,kubernetes.io/os=linux
host-2       Ready    <none>   71d   v1.18.2   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=host-2,kubernetes.io/os=linux
ubuntu1604   Ready    master   71d   v1.18.2   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=ubuntu1604,kubernetes.io/os=linux,node-role.kubernetes.io/master=

# Label removed from node but the pod still remains on the same node
$ kubectl get pod node-label-pod -n jul29 -o jsonpath='{.spec.nodeName}{"\n"}'
host-2
