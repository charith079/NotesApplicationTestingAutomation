pipeline {

    agent any

    environment {
        GRID_URL = "http://localhost:4444/wd/hub"
    }

    stages {

        // ==========================================
        // Checkout Code
        // ==========================================
        stage('Checkout Code') {
            steps {

                git branch: 'master',
                    url: 'https://github.com/charith079/NotesApplicationTestingAutomation.git'
            }
        }

        // ==========================================
        // Start Selenium Grid
        // ==========================================
        stage('Start Selenium Grid using Docker') {
            steps {

                sh '''
                docker-compose down --remove-orphans || true

                docker rm -f selenium-hub chrome firefox || true

                docker-compose up -d
                '''
            }
        }

        // ==========================================
        // Wait for Selenium Grid
        // ==========================================
        stage('Wait for Selenium Grid') {
            steps {

                sh '''
                echo "Waiting for Selenium Grid..."

                sleep 20

                curl http://localhost:4444/status
                '''
            }
        }

        // ==========================================
        // Install Python Dependencies
        // ==========================================
        stage('Install Dependencies') {
            steps {

                sh '''
                python3 -m pip install --upgrade pip

                pip3 install -r requirements.txt
                '''
            }
        }

        // ==========================================
        // Create Required Folders
        // ==========================================
        stage('Create Folders') {
            steps {

                sh '''
                mkdir -p Reports
                mkdir -p Screenshots
                mkdir -p Logs
                mkdir -p allure-results
                '''
            }
        }

        // ==========================================
        // Run Parallel Tests
        // ==========================================
        stage('Run Parallel Tests on Docker Grid (4 Workers)') {
            steps {

                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {

                    sh '''
                    export GRID_URL=http://localhost:4444/wd/hub

                    pytest -n 4 \
                    --html=Reports/report.html \
                    --self-contained-html \
                    --alluredir=allure-results
                    '''
                }
            }
        }

        // ==========================================
        // Archive Results
        // ==========================================
        stage('Archive Results') {
            steps {

                archiveArtifacts artifacts: 'Reports/*',
                                allowEmptyArchive: true

                archiveArtifacts artifacts: 'Screenshots/*',
                                allowEmptyArchive: true

                archiveArtifacts artifacts: 'Logs/*',
                                allowEmptyArchive: true
            }
        }

        // ==========================================
        // Generate Allure Report
        // ==========================================
        stage('Allure Report') {
            steps {

                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    // ==========================================
    // Post Actions
    // ==========================================
    post {

        always {

            sh 'docker-compose down'
        }

        success {

            echo "Tests Passed Successfully"
        }

        failure {

            echo "Tests Failed - Check Reports"
        }
    }
}