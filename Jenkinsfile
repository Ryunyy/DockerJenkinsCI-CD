pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr:'10', artifactNumToKeepStr:'10', daysToKeepStr:'20', artifactDaysToKeepStr:'20'))
  }
  stages {
    stage("Redfish test"){
      steps {
        sh '''
        qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/var/jenkins_home/workspace/PyTests_CI_CD/romulus/obmc-phosphor-image-romulus-20250520091100.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu &
        QEMU_PID=$!
        
        if ! kill -0 "$QEMU_PID" 2>/dev/null; then
            echo "QEMU exited unexpectedly."
            exit 1
        fi
        sleep 100s

         pytest --junit-xml="/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/redfish_report.xml" --disable-warnings -rf /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/redfish_pytest.py
        '''
      }
    }
    stage("Locust test") {
      steps {
        sh '''
        qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/var/jenkins_home/workspace/PyTests_CI_CD/romulus/obmc-phosphor-image-romulus-20250520091100.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu &
        QEMU_PID=$!
        
        if ! kill -0 "$QEMU_PID" 2>/dev/null; then
            echo "QEMU exited unexpectedly."
            exit 1
        fi
        sleep 100s

        locust --headless --json --skip-log > /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report.json -f /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/locustfile.py --host https://0.0.0.0:2443 --users 20 -r 5 -t 3m -s 20 --exit-code-on-error 0 
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
        sleep 100s

        pytest --junit-xml="/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/obmc_auth_report.xml" --disable-warnings /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/openbmc_auth_test.py
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
