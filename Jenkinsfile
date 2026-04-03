pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        echo 'Checking out code...'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t platform-log-service .'
      }
    }
    stage('Run Tests') {
      steps {
        sh '''
          docker run --rm platform-log-service python3 -m pytest -v
        '''
      }
    }
    stage('Stop Old Container') {
      steps {
        sh 'docker rm -f platform-app || true'
      }
    }

    stage('Run New Container') {
      steps {
        sh 'docker run -d -p 5000:5000 --name platform-app platform-log-service'
      }
    }
  }
}
