pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr:'10', artifactNumToKeepStr:'10', daysToKeepStr:'20', artifactDaysToKeepStr:'20'))
  }
  stages {
    stage("Enviroment Configuration") {
      when{
        expression {
          !fileExists('/var/jenkins_home/workspace/PyTests_CI_CD/initComlpete.txt')
        }
      }
      steps{
        sh '''
          apt-get update -y
          apt-get upgrade -y
          apt-get install qemu-system-arm -y
          apt-get install ipmitool -y
          apt-get install python3 -y
          apt-get install python3-pytest -y
          apt-get install python3-loguru -y
          apt-get install python3-selenium -y
          apt-get install python3-locust -y

          ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user set name 10 testuser
          ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user set password 10 [user10]
          ipmitool -C 17 -H localhost -p 2623 -I lanplus -U root -P 0penBmc user enable 10
          PATH=$PATH:/var/jenkins_home/workspace/PyTests_CI_CD/MEDriver/

          touch /var/jenkins_home/workspace/PyTests_CI_CD/initComlpete.txt
        '''
      }
    }
    stage("Qemu launch"){
      steps{
        sh '''
          qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/var/jenkins_home/workspace/PyTests_CI_CD/romulus/obmc-phosphor-image-romulus-20250520091100.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu &
          QEMU_PID=$!

          if ! kill -0 "$QEMU_PID" 2>/dev/null; then
            echo "QEMU exited unexpectedly."
            exit 1
          fi
          sleep 180s #waiting while qemu starts
        '''
      }
    }
    // stage("Redfish test"){
    //   steps {
    //     sh '''
    //      pytest --junit-xml="/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/redfish_report.xml" --disable-warnings -rf /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/redfish_pytest.py
    //     '''
    //   }
    // }
    stage("Locust test") {
      steps {
        sh '''
        locust --headless -f /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/locustfile.py --host http://127.0.0.1:2443 --users 50 -r 10 -t 3m -s 20 --exit-code-on-error 0 #--json --skip-log > /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report.json
        '''
      }
    }
    stage("OpenBMC Auth test"){
      steps {
        sh '''
        #busctl set-property xyz.openbmc_project.User.Manager/xyz/openbmc_project/user xyz.openbmc_project.User.AccountPolicy MaxLoginAttemptBeforeLockout q 3
        sleep 5s
        pytest --junit-xml="/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/obmc_auth_report.xml" --disable-warnings /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/openbmc_auth_test.py
        sleep 5s
        #busctl set-property xyz.openbmc_project.User.Manager/xyz/openbmc_project/user xyz.openbmc_project.User.AccountPolicy MaxLoginAttemptBeforeLockout q 100
        '''
      }
    }
  }
  post {
    success {
      junit '**/TestReports/*.xml'
    }
  }
}
