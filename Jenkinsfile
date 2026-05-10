pipeline {
    agent any

    environment {
        GRID_URL = "http://localhost:4444/wd/hub"
        PYTHONUNBUFFERED = "1"
    }

    options {
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // =========================================================
        // Checkout Source Code
        // =========================================================
        stage('Checkout Code') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/charith079/NotesApplicationTestingAutomation.git'
            }
        }

        // =========================================================
        // Start Selenium Grid
        // =========================================================
        stage('Start Selenium Grid using Docker') {
            steps {
                bat '''
                echo ==========================================
                echo Starting Selenium Grid...
                echo ==========================================

                docker-compose down --remove-orphans
                docker rm -f selenium-hub chrome firefox >nul 2>&1

                docker-compose up -d

                docker ps
                '''
            }
        }

        // =========================================================
        // Wait Until Grid Is Ready
        // =========================================================
        stage('Wait for Selenium Grid') {
            steps {
                powershell '''
                Write-Host "Waiting for Selenium Grid..."

                $url = "http://localhost:4444/status"

                for ($i = 0; $i -lt 30; $i++) {
                    try {
                        $response = Invoke-WebRequest -Uri $url -UseBasicParsing

                        if ($response.StatusCode -eq 200) {
                            Write-Host "Grid is UP"
                            exit 0
                        }
                    }
                    catch {
                        Write-Host "Waiting... attempt $i"
                    }

                    Start-Sleep -Seconds 5
                }

                Write-Host "Grid NOT ready"
                exit 1
                '''
            }
        }

        // =========================================================
        // Install Dependencies
        // =========================================================
        stage('Install Dependencies') {
            steps {
                bat '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        // =========================================================
        // Create Required Folders
        // =========================================================
        stage('Create Folders') {
            steps {
                bat '''
                if not exist Reports mkdir Reports
                if not exist screenshots mkdir screenshots
                if not exist logs mkdir logs
                if not exist allure-results mkdir allure-results
                '''
            }
        }

        // =========================================================
        // Run Tests
        // =========================================================
        stage('Run Parallel Tests on Docker Grid') {
            steps {

                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {

                    bat '''
                    echo ==========================================
                    echo Running Pytest Automation Suite
                    echo ==========================================

                    set GRID_URL=http://localhost:4444/wd/hub

                    pytest -n 4 ^
                    --html=Reports/report.html ^
                    --self-contained-html ^
                    --capture=tee-sys ^
                    --alluredir=allure-results
                    '''
                }
            }
        }

        // =========================================================
        // Publish HTML Report
        // =========================================================
        stage('Publish HTML Report') {
            steps {

                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'Reports',
                    reportFiles: 'report.html',
                    reportName: 'PyTest HTML Report'
                ])
            }
        }

        // =========================================================
        // Archive Reports / Screenshots / Logs
        // =========================================================
        stage('Archive Test Artifacts') {
            steps {

                archiveArtifacts artifacts: 'Reports/**/*',
                                 allowEmptyArchive: true

                archiveArtifacts artifacts: 'screenshots/**/*',
                                 allowEmptyArchive: true

                archiveArtifacts artifacts: 'logs/**/*',
                                 allowEmptyArchive: true

                archiveArtifacts artifacts: 'allure-results/**/*',
                                 allowEmptyArchive: true
            }
        }

        // =========================================================
        // Generate Allure Report
        // =========================================================
        stage('Allure Report') {
            steps {

                allure([
                    includeProperties: false,
                    jdk: '',
                    commandline: 'allure',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    // =============================================================
    // Post Actions
    // =============================================================
    post {

        always {

            echo "Stopping Docker Grid..."

            bat '''
            docker-compose down
            '''
        }

        success {
            echo "Tests Passed Successfully"
        }

        unstable {
            echo "Some Tests Failed - Check Reports"
        }

        failure {
            echo "Build Failed"
        }
    }
}