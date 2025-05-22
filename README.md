# DockerJenkinsCI-CD

1. ```docker network create jenkins```

2. ```docker volume create jenkins-docker-certs```
   
3. ```docker volume create jenkins-data```

docker container run \
   --name jenkins-docker \
   --detach \
   --privileged \
   --network jenkins
   --network-alias docker \
   --env DOCKER_TLS_CERTDIR=/certs \
   --volume jenkins-docker-certs:/certs/client \
   --volume jenkins-data:/var/jenkins_home \
   --publish 2376:2376 \
   docker:dind
   
```docker container run --name jenkins-docker --detach --privileged --network jenkins --network-alias docker --env DOCKER_TLS_CERTDIR=/certs --volume jenkins-docker-certs:/certs/client --volume jenkins-data:/var/jenkins_home --publish 2376:2376 docker:dind```

docker container run \
   --name jenkins-myocean \
   --detach --network jenkins \
   --env DOCKER_HOST=tcp://docker:2376 \
   --env DOCKER_CERT_PATH=/certs/client \
   --env DOCKER_TLS_VERIFY=1 \
   --publish 8080:8080 \
   --publish 50000:50000 \
   --volume jenkins-data:/var/jenkins_home \
   --volume jenkins-docker-certs:/certs/client:ro \
   jenkins/jenkins:lts-jdk17
   
```docker container run --name jenkins-myocean --detach --network jenkins --env DOCKER_HOST=tcp://docker:2376 --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 --publish 8080:8080 --publish 50000:50000 --volume jenkins-data:/var/jenkins_home --volume jenkins-docker-certs:/certs/client:ro jenkins/jenkins:lts-jdk17```

```docker container exec -u root -it jenkins-myocean /bin/bash```

```apt-get update```

```apt-get upgrade```

```apt install qemu-system-arm```

```apt-get install ipmitool```

```apt-get install python3```

```apt-get install python3-pip```

```apt-get install python3-venv```

```mkdir /python_venv/```

```python3 -m venv /python_env/```

```source /python_env/bin/activate```

```pip install pytest loguru locust selenium```

```qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/var/jenkins_home/workspace/PyTests_CI_CD/romulus/obmc-phosphor-image-romulus-20250520091100.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu```

При запущеном QEMU:

```ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user set name 10 testuser```

```ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user set password 10 [user10]```

```ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user enable 10```

```busctl set-property xyz.openbmc_project.User.Manager/xyz/openbmc_project/user xyz.openbmc_project.User.AccountPolicy MaxLoginAttemptBeforeLockout q 3```

```busctl set-property xyz.openbmc_project.User.Manager/xyz/openbmc_project/user xyz.openbmc_project.User.AccountPolicy MaxLoginAttemptBeforeLockout q 100```

```PATH=$PATH:/var/jenkins_home/workspace/PyTests_CI_CD/MEDriver/```
