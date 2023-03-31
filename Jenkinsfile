pipeline {
  agent any
  stages {
    stage('Check requirements') {
      steps {
        script {
          def requirements = sh(returnStdout: true, script: 'pip freeze | grep requests')
          if (requirements.contains('requests')) {
            echo 'Requirements already installed'
          } else {
            echo 'Installing requirements'
            sh 'pip install requests'
          }
        }
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
