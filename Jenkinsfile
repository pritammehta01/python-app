pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub-cred')
        IMAGE = "pritammehta/pythonapp"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/pritammehta01/python-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE}:${BUILD_NUMBER} .
                """
            }
        }

        stage('DockerHub Login') {
            steps {
                sh """
                echo ${DOCKERHUB_PSW} | docker login -u ${DOCKERHUB_USR} --password-stdin
                """
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh """
                docker push ${IMAGE}:${BUILD_NUMBER}
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                kubectl set image deployment/python-deployment pythonapp=${IMAGE}:${BUILD_NUMBER}
                kubectl rollout status deployment/python-deployment
                """
            }
        }
    }

    post {
        success {
            echo "Deployed NEW image version: ${BUILD_NUMBER}"
        }
        failure {
            echo "Deployment FAILED."
        }
    }
}
