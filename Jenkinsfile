pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr:'10', artifactNumToKeepStr:'10', daysToKeepStr:'20', artifactDaysToKeepStr:'20'))
  }
  stages {
    stage("Locust test") {
      steps {
        sh '''
        qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/var/jenkins_home/workspace/PyTests_CI_CD/romulus/obmc-phosphor-image-romulus-20250520091100.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu &
        QEMU_PID=$!
        
        if ! kill -0 "$QEMU_PID" 2>/dev/null; then
            echo "QEMU exited unexpectedly."
            exit 1
        fi
        sleep 95s

        locust -f /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/locustfile.py --headless --users 20 --spawn-rate 5 --run-time 3m --stop-timeout 20 --host https://127.0.0.1:2443 --exit-code-on-error 0 --json --skip-log > /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report.json
        '''
      }
    }
    stage("Redfish test"){
      steps {
        sh '''
        qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/var/jenkins_home/workspace/PyTests_CI_CD/romulus/obmc-phosphor-image-romulus-20250520091100.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu &
        QEMU_PID=$!
        
        if ! kill -0 "$QEMU_PID" 2>/dev/null; then
            echo "QEMU exited unexpectedly."
            exit 1
        fi
        sleep 95s

         pytest --junit-xml="/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/redfish_report.xml" --disable-warnings -rf /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/redfish_pytest.py
        '''
      }
    }
    stage("OpenBMC Auth test"){
      steps {
        sh '''
        . /venv_obmc/bin/activate
        qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/var/jenkins_home/workspace/PyTests_CI_CD/romulus/obmc-phosphor-image-romulus-20250520091100.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu &
        QEMU_PID=$!
        
        if ! kill -0 "$QEMU_PID" 2>/dev/null; then
            echo "QEMU exited unexpectedly."
            exit 1
        fi
        sleep 95s

        pytest --junit-xml="/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/obmc_auth_report.xml" --disable-warnings /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/openbmc_auth_test.py
        '''
      }
    }
  }
  post {
    success {
      junit '**/reports/*.xml'
    }
  }
}
