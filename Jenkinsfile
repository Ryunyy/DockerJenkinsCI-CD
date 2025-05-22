pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr:'10', artifactNumToKeepStr:'10', daysToKeepStr:'20', artifactDaysToKeepStr:'20'))
  }
  stages {
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
    stage("Redfish test"){
      steps {
        sh '''
         . /python_env/bin/activate
         pytest --junit-xml="/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/redfish_report.xml" --disable-warnings -rf /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/redfish_pytest.py
        '''
      }
    }
    stage("OpenBMC Auth test"){
      steps {
        sh '''
        . /python_env/bin/activate
        pytest --junit-xml="/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/obmc_auth_report.xml" --disable-warnings /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/openbmc_auth_test.py
        '''
      }
    }
    stage("Locust test") {
      steps {
        sh '''
        . /python_env/bin/activate
        locust --headless -f /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/locustfile.py --host https:/ --users 20 -r 3 -t 2m -s 20 --html /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report_20.html --exit-code-on-error 0 --json --skip-log > /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report_20.json
        locust --headless -f /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/locustfile.py --host https:/ --users 50 -r 10 -t 2m -s 20 --html /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report_50.html --exit-code-on-error 0 --json --skip-log > /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report_50.json
        locust --headless -f /var/jenkins_home/workspace/PyTests_CI_CD/TestFiles/locustfile.py --host https:/ --users 70 -r 20 -t 2m -s 20 --html /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report_70.html --exit-code-on-error 0 --json --skip-log > /var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_report_70.json
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
