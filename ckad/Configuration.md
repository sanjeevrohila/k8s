# Configmap
  - Create
  - Describe



### Create configmap

```
$ kubectl create configmap myconfig --from-literal=key1=val1 --from-literal=key2=val2 --dry-run -o yaml
apiVersion: v1
data:
  key1: val1
  key2: val2
kind: ConfigMap
metadata:
  creationTimestamp: null
  name: myconfig
```

### Describe configmap
```
$ kubectl describe configmap myconfig
Name:         myconfig
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
key1:
----
val1
key2:
----
val2
Events:  <none>
```


# Create pod with environmant Variables (imperative way)
```
$ kubectl run mypod --image=nginx --port=80 --restart=Never --env={key1=val1,key2=val2} --dry-run -o yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: mypod
  name: mypod
spec:
  containers:
  - env:
    - name: key1
      value: val1
    - name: key2
      value: val2
    image: nginx
    name: mypod
    ports:
    - containerPort: 80
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}
```


# Pass config map to a pod container to se the env Variable

```
$ cat pod-from-config.yaml 
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: mypod
  name: mypod
spec:
  containers:
  - image: nginx
    name: mypod
    ports:
    - containerPort: 80
    envFrom:
    - configMapRef:
        name: myconfig
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}
```
