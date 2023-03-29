pipeline {
  agent any
  stages {
    stage('Install requirements') {
            steps {
                sh 'pip install requests'
            }
        }
    stage('Monitoring Your LAN') {
      steps {
        sh 'python3 LAN_Monitor.py'
      }
    }
    stage('Monitoring Your WAN') {
      steps {
        sh 'python3 WAN_Monitor.py'
      }
    }
  }
}
