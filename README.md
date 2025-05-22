# DockerJenkinsCI-CD. МГ-311 Сентюров Святослав

### Для выполнения задания нам понадобится установить докер на вашу рабочую (хост) машину (в моем случае это docker.desktop) и нстроить два докера: один dind, второй с jenkins. Для этого сначала создадим общую для них сеть:

```docker network create jenkins```

### Затем определим для них тома:

1. ```docker volume create jenkins-docker-certs```
   
2. ```docker volume create jenkins-data```

### Пришло время запустить наши контейнеры с подгрузкой образов, определением портов, сетей и томов. Первый докер dind и его команда выглядит так:

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

### А это его же команда, которую нужно скопировать и запустить в командной строке
   
```docker container run --name jenkins-docker --detach --privileged --network jenkins --network-alias docker --env DOCKER_TLS_CERTDIR=/certs --volume jenkins-docker-certs:/certs/client --volume jenkins-data:/var/jenkins_home --publish 2376:2376 docker:dind```

### Это команда для докера с Jenkins

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

### Теперь для далнейшей настройки нам нужно зайти в докер с Jenkins пот пользователем root и выполнить первоначальную установку зависимостей. Это можно указать и в самом Jenkinsfile, но в моем случае в качестве агента ипользуется лишь python.

### Итак, команда для root:

```docker container exec -u root -it jenkins-myocean /bin/bash```

### А теперь выполняем установку зависимостей вручную в таком порядке, в каком они указаны внизу:

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

### С настройкой зависимостей закончили, теперь для успешного прохождения тестов аутентификации Selenium-а нам надо запустить QEMU из образа, который есть в репозитории и создать пользователя.
### Запускаем QEMU следующей командой:

```qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/var/jenkins_home/workspace/PyTests_CI_CD/romulus/obmc-phosphor-image-romulus-20250520091100.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu```

### Теперь нужно немного подождать, пока QEMU не предложет войти под пользователем root. Когда это произошло, в другом терминале (в этом же докере, но другом терминале) нужно прописать команды создания нового пользователя:

1. ```ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user set name 10 testuser```

2. ```ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user set password 10 [user10]```

3. ```ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user enable 10```

### Пользователь создан и для тестов нам нужно ограничить его количество неудачных входов командой. В данной команде ему дается 3 попытки.

```busctl set-property xyz.openbmc_project.User.Manager/xyz/openbmc_project/user xyz.openbmc_project.User.AccountPolicy MaxLoginAttemptBeforeLockout q 3```

### После тестов можно вернуть ему больше попыток, но перед тестами обязательно нужно выполняь команду выше. Команда установки 100 попыток приведена ниже:

```busctl set-property xyz.openbmc_project.User.Manager/xyz/openbmc_project/user xyz.openbmc_project.User.AccountPolicy MaxLoginAttemptBeforeLockout q 100```

## Установка Microsoft Edge и его веб-драйвера
### В работе используется драйвер msedgedriver, поэтому нам нудно настроить сам браузер. которого по умолчанию нет. Для этого используем следующие команды, которые добавляют в пути для получения обновлений ссылку на пакеты microsoft:

```curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg```
```install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/```
```sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list'```
```rm microsoft.gpg```

### Обязательно обновляем список командой

```apt update```

### И ставим последнюю версию браузера

```apt install microsoft-edge-stable```

### Проверяем его версию командой

```microsoft-edge --version```

### В моем случае, версия Microsoft Edge 136.0.3240.76, а значит и драйвер надо ставить версии 136.0.3240. В моем случае я имею этот драйвер в папке MSDriver.

### Теперь нужно добавить папку с драйвером в переменные окружения, поэтому используем команду ниже:

```PATH=$PATH:/var/jenkins_home/workspace/PyTests_CI_CD/MEDriver/```
