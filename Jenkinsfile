pipeline {
    agent any

    environment {
        GRID_URL = "http://localhost:4444/wd/hub"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/charith079/NotesApplicationTestingAutomation.git'
            }
        }

        stage('Start Selenium Grid using Docker') {
            steps {
                bat '''
                docker-compose down --remove-orphans
                docker rm -f selenium-hub chrome firefox || exit 0
                docker-compose up -d
                '''
            }
        }

        stage('Wait for Selenium Grid') {
            steps {
                bat '''
                echo Waiting for Selenium Grid to start...

                powershell -Command ^
                "for ($i=0; $i -lt 30; $i++) { ^
                    try { ^
                        $r = Invoke-WebRequest http://localhost:4444/status -UseBasicParsing; ^
                        if ($r.StatusCode -eq 200) { ^
                            Write-Output 'Grid is UP'; ^
                            exit 0 ^
                        } ^
                    } catch {} ^
                    Start-Sleep -Seconds 5 ^
                } ^
                Write-Output 'Grid NOT ready'; exit 1"
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Create Folders') {
            steps {
                bat '''
                if not exist Reports mkdir Reports
                if not exist Screenshots mkdir Screenshots
                if not exist Logs mkdir Logs
                if not exist allure-results mkdir allure-results
                '''
            }
        }

        stage('Run Parallel Tests on Docker Grid (4 Workers)') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat '''
                    set GRID_URL=http://localhost:4444/wd/hub
                    pytest -n 4 ^
                    --html=Reports/report.html ^
                    --self-contained-html ^
                    --alluredir=allure-results
                    '''
                }
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'Reports/*', allowEmptyArchive: true
                archiveArtifacts artifacts: 'Screenshots/*', allowEmptyArchive: true
                archiveArtifacts artifacts: 'Logs/*', allowEmptyArchive: true
            }
        }

        stage('Allure Report') {
            steps {
                allure([
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            bat 'docker-compose down'
        }

        success {
            echo "Tests Passed Successfully"
        }

        failure {
            echo "Tests Failed - Check Reports"
        }
    }
}