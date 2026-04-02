pipeline {
  agent any

  stages {
    stage('Checkout confirmation') {
      steps {
        echo 'Jenkins started from a GitHub-triggered pipeline.'
        sh 'pwd'
        sh 'ls -la'
      }
    }

    stage('Python check') {
      steps {
        sh 'python3 --version || python --version || true'
      }
    }
  }
}
