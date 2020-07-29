Get all images in all pods:
```sh
$ for ele in `kubectl get po -o jsonpath='{.items[*].spec.containers[*].image}'`; do echo $ele; done
```

### Create Multi container pod
### Exec into pod and runn command
### Update the container image
### record and check rollout history
### rollback

Create multi container pod
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


