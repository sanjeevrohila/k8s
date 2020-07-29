Get all images in all pods:
```sh
$ for ele in `kubectl get po -o jsonpath='{.items[*].spec.containers[*].image}'`; do echo $ele; done
```




### Multi container Pod

 - Create Multi container pod
 - Exec into pod and runn command
 - Update the container image
 - Record and check rollout history
 - Rollback


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
