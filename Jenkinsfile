pipeline {
  agent any

  environment {
    WEB_APP_FINERACT_API_URL = 'http://fineract-server:8080'
  }

  options {
    ansiColor('xterm')
    timestamps()
  }

  stages {
    stage('Start Compose Stack') {
      steps {
        dir('mifosx-platform') {
          sh '''
            docker compose up -d --build
          '''
        }
      }
    }

    stage('Run Pytest') {
      steps {
        dir('mifosx-platform') {
          script {
            catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
              sh '''
                docker compose exec -T test-runner sh -c 'cd /app/database-setup && mkdir -p test-results && python -m pytest --junitxml=test-results/pytest-results.xml'
              '''
            }
            sh '''
              mkdir -p ../test-results
              CONTAINER=$(docker compose ps -q test-runner)
              docker cp "$CONTAINER":/app/database-setup/test-results/pytest-results.xml ../test-results/pytest-results.xml || true
            '''
          }
        }
      }
    }

    stage('Publish JUnit Results') {
      steps {
        junit allowEmptyResults: true, testResults: 'test-results/pytest-results.xml'
      }
    }
  }

  post {
    always {
      dir('mifosx-platform') {
        sh '''
          docker compose down -v
        '''
      }
    }
  }
}
