pipeline {
  agent any

  environment {
    COMPOSE_PROFILES = 'test'
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
            docker compose up -d --build test-runner
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

    stage('Run Newman API Tests') {
      steps {
        dir('mifosx-platform') {
          script {
            catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
              sh '''
                docker compose exec -T test-runner sh -c 'cd /app/api-tests && mkdir -p test-results && newman run "MifosX Fineract API Tests.postman_collection.json" --env-var baseUrl="${SERVER_URL}/fineract-provider/api/v1" --reporters cli,junit,htmlextra --reporter-junit-export test-results/newman-results.xml --reporter-htmlextra-export test-results/newman-report.html'
              '''
            }
            sh '''
              mkdir -p ../test-results
              CONTAINER=$(docker compose ps -q test-runner)
              docker cp "$CONTAINER":/app/api-tests/test-results/newman-results.xml ../test-results/newman-results.xml || true
              docker cp "$CONTAINER":/app/api-tests/test-results/newman-report.html ../test-results/newman-report.html || true
            '''
          }
        }
      }
    }

    stage('Run Playwright UI Tests') {
      steps {
        dir('mifosx-platform') {
          script {
            catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
              sh '''
                docker compose exec -T test-runner sh -c 'cd /app/ui-tests && mkdir -p test-results && CI=true npx playwright test'
              '''
            }
            sh '''
              mkdir -p ../test-results
              CONTAINER=$(docker compose ps -q test-runner)
              docker cp "$CONTAINER":/app/ui-tests/test-results/playwright-results.xml ../test-results/playwright-results.xml || true
              mkdir -p ../test-results/playwright-report
              docker cp "$CONTAINER":/app/ui-tests/playwright-report/. ../test-results/playwright-report || true
            '''
          }
        }
      }
    }

    stage('Publish JUnit Results') {
      steps {
        junit allowEmptyResults: true, testResults: 'test-results/*.xml'
      }
    }

    stage('Publish HTML Reports') {
      steps {
        publishHTML([
          allowMissing: true,
          alwaysLinkToLastBuild: true,
          keepAll: true,
          reportDir: 'test-results',
          reportFiles: 'newman-report.html',
          reportName: 'Newman API Report'
        ])
        publishHTML([
          allowMissing: true,
          alwaysLinkToLastBuild: true,
          keepAll: true,
          reportDir: 'test-results/playwright-report',
          reportFiles: 'index.html',
          reportName: 'Playwright UI Report'
        ])
        archiveArtifacts allowEmptyArchive: true, artifacts: 'test-results/newman-report.html,test-results/playwright-report/**', fingerprint: true
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
