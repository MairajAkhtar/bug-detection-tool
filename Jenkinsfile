pipeline {
    agent any

    environment {
        IMAGE_NAME = 'bug-detection-tool'
        CONTAINER_NAME = 'bug-detection-app'
        PORT = '5000'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone your main branch (update URL if needed)
                git branch: 'main', url: 'https://github.com/MairajAkhtar/bug-detection-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image (Dockerfile handles model download)
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Stop Previous Container') {
            steps {
                script {
                    // Stop and remove previous container if running
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the new container, map port 5000
                    sh "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}"
                }
            }
        }
    }
}
