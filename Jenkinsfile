pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
        COMPOSE_PROJECT_NAME = "pythonapp"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/pritammehta01/Safe-Credential.git'
            }
        }

        stage('Docker Login') {
            steps {
                sh '''
                echo $DOCKER_HUB_CREDENTIALS_PSW | docker login -u $DOCKER_HUB_CREDENTIALS_USR --password-stdin
                '''
            }
        }

        stage('Pull Images') {
            steps {
                sh '''
                docker pull 34.121.95.79:5000/pythonapp:latest
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                docker-compose down
                docker-compose up -d
                '''
            }
        }

        stage('Cleanup Old Images') {
            steps {
                sh '''
                docker image prune -f
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
            sh 'docker ps'
        }
        failure {
            echo '❌ Deployment failed.'
        }
    }
}
