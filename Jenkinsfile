pipeline {
    agent any

    // Tool versions configured in Jenkins → Manage Jenkins → Tools
    tools {
        jdk 'jdk17'
        maven 'maven3'
    }

    // Variables used across all stages
    environment {
        // Replace with your actual ECR URI from Phase 10.3
        ECR_REPO    = '079716037028.dkr.ecr.ap-south-1.amazonaws.com/employee-api'
        AWS_REGION  = 'ap-south-1'
        CLUSTER     = 'devops-demo'
        // BUILD_NUMBER is automatically set by Jenkins (1, 2, 3...)
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
    }

    stages {

        // ─────────────────────────────────────────────
        // STAGE 1: Checkout code from GitHub
        // ─────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code from GitHub...'
                checkout scm
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 2: Build and run unit tests with Maven
        // ─────────────────────────────────────────────
        stage('Build & Unit Test') {
            steps {
                echo '🔨 Building application and running tests...'
                sh 'mvn clean verify'
            }
            post {
                always {
                    // Archive test results so Jenkins shows them in the UI
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 3: Analyze code with SonarQube
        // ─────────────────────────────────────────────
        stage('SonarQube Analysis') {
            steps {
                echo '🔍 Sending code to SonarQube for analysis...'
                withSonarQubeEnv('SonarQubeServer') {
                    sh 'mvn sonar:sonar'
                }
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 4: Wait for SonarQube Quality Gate
        // Pipeline will STOP here if code quality is bad
        // ─────────────────────────────────────────────
        stage('Quality Gate') {
            steps {
                echo '🚦 Waiting for SonarQube Quality Gate result...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 5: Build Docker image and push to ECR
        // ─────────────────────────────────────────────
        stage('Docker Build & Push') {
            steps {
                echo "🐳 Building Docker image: ${ECR_REPO}:${IMAGE_TAG}"
                sh """
                  # Login to ECR
                  aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_REPO}

                  # Build the image
                  docker build -t ${ECR_REPO}:${IMAGE_TAG} .

                  # Also tag it as 'latest'
                  docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REPO}:latest

                  # Push both tags
                  docker push ${ECR_REPO}:${IMAGE_TAG}
                  docker push ${ECR_REPO}:latest

                  echo "✅ Image pushed: ${ECR_REPO}:${IMAGE_TAG}"
                """
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 6: Deploy to EKS
        // ─────────────────────────────────────────────
        stage('Deploy to EKS') {
            steps {
                echo "🚀 Deploying to EKS cluster: ${CLUSTER}"
                sh """
                  # Configure kubectl to use this cluster
                  aws eks update-kubeconfig --name ${CLUSTER} --region ${AWS_REGION}

                  # Apply Kubernetes manifests (creates deployment + service if not there)
                  kubectl apply -f k8s/deployment.yaml
                  kubectl apply -f k8s/service.yaml
                  kubectl apply -f k8s/hpa.yaml

                  # Update the image to the new build number
                  kubectl set image deployment/employee-api \
                    employee-api=${ECR_REPO}:${IMAGE_TAG}

                  # Wait until all pods are running the new version
                  kubectl rollout status deployment/employee-api --timeout=300s

                  echo "✅ Deployment complete!"
                  kubectl get pods
                  kubectl get svc employee-api-svc
                """
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 7: AI generates release notes
        // ─────────────────────────────────────────────
        stage('AI: Generate Release Notes') {
            steps {
                echo '🤖 Using AI to generate release notes...'
                withCredentials([
                    string(credentialsId: 'anthropic-api-key', variable: 'ANTHROPIC_API_KEY')
                ]) {
                    sh """
                      pip3 install anthropic --quiet --break-system-packages
                      python3 ai-assistant/generate_release_notes.py
                    """
                    // Archive the release notes as a build artifact
                    archiveArtifacts artifacts: 'RELEASE_NOTES.md', allowEmptyArchive: true
                    echo '✅ Release notes saved as build artifact'
                }
            }
        }
    }

    // ─────────────────────────────────────────────
    // POST: Runs after all stages complete or fail
    // ─────────────────────────────────────────────
    post {

        // If ANY stage fails, run AI failure analysis
        failure {
            echo '❌ Build FAILED — running AI failure analysis...'
            withCredentials([
                string(credentialsId: 'anthropic-api-key', variable: 'ANTHROPIC_API_KEY')
            ]) {
                sh """
                  pip3 install anthropic --quiet --break-system-packages

                  # Get the Jenkins console log
                  # Jenkins stores the log at: /var/lib/jenkins/jobs/<job>/builds/<num>/log
                  LOG_PATH="/var/lib/jenkins/jobs/${JOB_NAME}/builds/${BUILD_NUMBER}/log"

                  if [ -f "\$LOG_PATH" ]; then
                    python3 ai-assistant/analyze_failure.py "\$LOG_PATH"
                  else
                    echo "Log file not found at \$LOG_PATH" > ai_failure_summary.md
                    echo "Trying workspace..." >> ai_failure_summary.md
                  fi
                """
                archiveArtifacts artifacts: 'ai_failure_summary.md', allowEmptyArchive: true
            }
        }

        // Always clean up Docker images to save disk space
        always {
            sh """
              docker rmi ${ECR_REPO}:${IMAGE_TAG} || true
              docker rmi ${ECR_REPO}:latest || true
              docker system prune -f || true
            """
        }

        success {
            echo '✅ Pipeline completed successfully!'
        }
    }
}