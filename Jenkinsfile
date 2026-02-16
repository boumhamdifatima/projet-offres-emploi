pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
    }
    stages {
        stage('Install') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Scraping') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    python3 scraper.py
                '''
            }
        }
        stage('DetectChanges') {
            steps {
                script {
                    def current = "data/jobs.csv"
                    def previous = "data/jobs_previous.csv"
                    if (fileExists(previous)) {
                        def diff = sh(script: "diff ${current} ${previous} || true", returnStdout: true).trim()
                        if (diff == "") {
                            echo "Aucun changement détecté. Fin du pipeline."
                            currentBuild.result = 'SUCCESS'
                            error("Pipeline arrêté : pas de nouvelles offres.")
                        }
                    }
                    sh "cp ${current} ${previous}"
                }
            }
        }
        stage('Conversion') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    python3 html_generator.py
                '''
            }
        }
        stage('Tests') {
            steps {
                sh '''
                    line_count=$(wc -l < data/jobs.csv)
                    if [ "$line_count" -lt 10 ]; then echo "Moins de 10 offres"; exit 1; fi
                    grep -q "<table>" public/index.html
                '''
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'data/*.csv, public/*.html, logs/*.txt', allowEmptyArchive: true
            }
        }
        stage('Deploy with Docker') {
            steps {
                sh '''
                    # Arrêter et supprimer l'ancien conteneur s'il existe
                    docker stop job-server || true
                    docker rm job-server || true
                    
                    # Construire la nouvelle image avec le dernier index.html
                    docker build -t mes-offres-emploi .
                    
                    # Lancer le conteneur sur le port 8081 (pour ne pas entrer en conflit avec Jenkins sur 8080)
                    docker run -d --name job-server -p 8081:80 mes-offres-emploi
                '''
                echo "Application déployée sur http://votre-ip:8081"
            }
        }
    }
    post {
        always {
            sh "rm -rf $VENV_DIR || true"
        }
    }
}