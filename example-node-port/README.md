# Example
`1- Deploy pods with 3 replicasets`
```
kubectl apply -f nginx-dep.yaml
```


`2- Deploy Service for the deployed pods where nginx servers running`
```
kubectl apply -f nginx-dep-svc.yaml
```

Create a service on nodeport which upon
calling with the UP Address of any  of the
node in cluster with the 30163, send the
resquest to any of the pod 

`3 - References`

https://matthewpalmer.net/kubernetes-app-developer/articles/service-kubernetes-example-tutorial.html
https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/

`4 - Check the deployment`
kubectl get deployment and pods

```
ubuntu@k8s-master:~$ kubectl get deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           23h
```

```
ubuntu@k8s-master:~$ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-6dd686cd46-6wkzh   1/1     Running   0          23h
nginx-deployment-6dd686cd46-ffngs   1/1     Running   0          23h
nginx-deployment-6dd686cd46-pk65g   1/1     Running   0          23h
```

`5 - describe deployment`

```
ubuntu@k8s-master:~$ kubectl describe deployment nginx-deployment
Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      Thu, 23 Apr 2020 11:42:31 -0700
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx-flask-application,tier=backend,track=stable
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx-flask-application
           tier=backend
           track=stable
  Containers:
   flask-container:
    Image:        nginx
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-deployment-6dd686cd46 (3/3 replicas created)
Events:          <none>
```


`6 - Scale the app by increasing the replicasets`
Edit the nginx-dep.yaml and change the below - 

```
replicas: 4
```
Now run the below command -

```
kubectl replace -f nginx-dep.yaml
```

Check the pods now - An `pod nginx-deployment-6dd686cd46-whkbt` is added

```
ubuntu@k8s-master:~$ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-6dd686cd46-6wkzh   1/1     Running   0          23h
nginx-deployment-6dd686cd46-ffngs   1/1     Running   0          23h
nginx-deployment-6dd686cd46-pk65g   1/1     Running   0          23h
nginx-deployment-6dd686cd46-whkbt   1/1     Running   0          17s
```


`7 - Now we need to check that the additional pod is also being request by the service`

Do add the ip to the HTML at each pod
```
ubuntu@k8s-master:~$ kubectl exec -it nginx-deployment-6dd686cd46-whkbt -- bash
root@nginx-deployment-6dd686cd46-whkbt:/# hostname -I
10.244.2.4
root@nginx-deployment-6dd686cd46-whkbt:/# cd /usr/share/nginx/html/
root@nginx-deployment-6dd686cd46-whkbt:/usr/share/nginx/html# sed -i 's/Welcome to nginx/Welcome to nginx - 10.10.2.4/g' index.html
```

`8 - Now run the script ouside at any console `
```
watch -n 1 "curl -sS -XGET http://10.20.30.2:30163/ | grep \"<h1>Welcome to nginx\" >> res.txt"
```

`9 - Verify the response by `

```
$ cat res.txt 
<h1>Welcome to nginx - 10.10.2.4!</h1>
<h1>Welcome to nginx - 10.10.1.2!</h1>
<h1>Welcome to nginx - 10.10.2.3!</h1>
<h1>Welcome to nginx - 10.10.2.4!</h1>
<h1>Welcome to nginx - 10.10.2.4!</h1>
<h1>Welcome to nginx - 10.10.1.2!</h1>
<h1>Welcome to nginx - 10.10.1.2!</h1>
```

We can observe that the response is recieved from four unique IPs

