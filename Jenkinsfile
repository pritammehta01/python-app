// pipeline {
//     agent any

//     environment {
//         DOCKERHUB = credentials('dockerhub-cred')
//         IMAGE = "pritammehta/pythonapp"
//     }

//     stages {

//         stage('Checkout Code') {
//             steps {
//                 git branch: 'main', url: 'https://github.com/pritammehta01/python-app.git'
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 sh """
//                 docker build -t ${IMAGE}:${BUILD_NUMBER} .
//                 """
//             }
//         }

//         stage('DockerHub Login') {
//             steps {
//                 sh """
//                 echo ${DOCKERHUB_PSW} | docker login -u ${DOCKERHUB_USR} --password-stdin
//                 """
//             }
//         }

//         stage('Push to DockerHub') {
//             steps {
//                 sh """
//                 docker push ${IMAGE}:${BUILD_NUMBER}
//                 """
//             }
//         }

//         stage('Deploy to Kubernetes') {
//             steps {
//                 sh """
//                 kubectl set image deployment/python-deployment pythonapp=${IMAGE}:${BUILD_NUMBER}
//                 kubectl rollout status deployment/python-deployment
//                 """
//             }
//         }
//     }

//     post {
//         success {
//             echo "Deployed NEW image version: ${BUILD_NUMBER}"
//         }
//         failure {
//             echo "Deployment FAILED."
//         }
//     }
// }


pipeline {
    agent any

    environment {
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
                docker tag ${IMAGE}:${BUILD_NUMBER} ${IMAGE}:latest
                """
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push ${IMAGE}:${BUILD_NUMBER}
                    docker push ${IMAGE}:latest
                    """
                }
            }
        }

        stage('Update Kubernetes Deployment') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                    kubectl --kubeconfig=$KUBECONFIG set image deployment/python-app pythonapp=${IMAGE}:${BUILD_NUMBER}
                    kubectl --kubeconfig=$KUBECONFIG rollout status deployment/python-app --timeout=120s

                    """
                }
            }
        }
    }

    post {
        success {
            echo "Deployed successfully: ${IMAGE}:${BUILD_NUMBER}"
        }
        failure {
            echo "Deployment failed."
        }
    }
}
