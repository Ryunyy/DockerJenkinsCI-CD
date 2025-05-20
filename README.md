# DockerJenkinsCI-CD

1. docker network create jenkins

2. docker volume create jenkins-docker-certs
   
3. docker volume create jenkins-data

1. docker container run --name jenkins-docker --detach --privileged --network jenkins --network-alias docker --env DOCKER_TLS_CERTDIR=/certs --volume jenkins-docker-certs:/certs/client --volume jenkins-data:/var/jenkins_home --publish 2376:2376 docker:dind

2. docker container run --name jenkins-myocean --detach --network jenkins --env DOCKER_HOST=tcp://docker:2376 --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 --publish 8080:8080 --publish 50000:50000 --volume jenkins-data:/var/jenkins_home --volume jenkins-docker-certs:/certs/client:ro jenkins/jenkins:lts-jdk17

apt-get update

apt install qemu-system-arm

apt-get install ipmitool

apt-get install python3

apt install python3-pip

apt-get install python3-pytest

apt-get install python3-loguru

apt install python3-locust

apt install python3-selenium


ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user set name 10 testuser

ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user set password 10 [user10]

ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user enable 10

busctl set-property xyz.openbmc_project.User.Manager/xyz/openbmc_project/user xyz.openbmc_project.User.AccountPolicy MaxLoginAttemptBeforeLockout q 3
