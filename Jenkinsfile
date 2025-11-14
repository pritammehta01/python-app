pipeline {
    agent any

    environment {
        REGISTRY_CREDENTIALS = credentials('private-docker-registry')   // Jenkins cred ID
        REGISTRY_URL = "34.121.95.79:5000"
        COMPOSE_PROJECT_NAME = "pythonapp"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/pritammehta01/python-app.git'
            }
        }

        stage('Docker Login to Private Registry') {
            steps {
                sh '''
                echo $REGISTRY_CREDENTIALS_PSW | docker login $REGISTRY_URL -u $REGISTRY_CREDENTIALS_USR --password-stdin
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                # Build local image from Dockerfile in repo
                docker build -t pythonapp:latest .

                # Tag for private registry (build-number and latest)
                docker tag pythonapp:latest $REGISTRY_URL/pythonapp:${BUILD_NUMBER}
                docker tag pythonapp:latest $REGISTRY_URL/pythonapp:latest
                '''
            }
        }

        stage('Push Image to Private Registry') {
            steps {
                sh '''
                docker push $REGISTRY_URL/pythonapp:${BUILD_NUMBER}
                docker push $REGISTRY_URL/pythonapp:latest
                '''
            }
        }

        stage('Pull Image (verify from registry)') {
            steps {
                sh '''
                docker pull $REGISTRY_URL/pythonapp:latest
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                # Ensure latest image from registry is used
                docker pull $REGISTRY_URL/pythonapp:latest

                # Bring down old containers (support both docker compose and docker-compose)
                docker-compose down || true

                # Bring up with new image
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
            echo 'Deployment successful!'
            sh 'docker ps'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}

