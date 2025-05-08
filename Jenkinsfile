pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                 git branch: 'main', url: 'https://github.com/MairajAkhtar/bug-detection-app.git'
            }
        }

        stage('Set Up Python') {
    steps {
        bat '''
            python -m venv venv
            call venv\\Scripts\\activate
            pip install -r requirements.txt
        '''
    }
}

       stage('Run Jenkins Prediction') {
    steps {
        bat '''
            call venv\\Scripts\\activate
            python -c "from app import model; import pandas as pd; df = pd.read_csv('uploads/metrics_from_jenkins.csv'); df['Predicted Bugs'] = model.predict(df); df.to_csv('uploads/predicted_from_jenkins.csv', index=False)"
        '''
    }
}

        stage('Archive Output') {
            steps {
                archiveArtifacts artifacts: 'uploads/predicted_from_jenkins.csv', fingerprint: true
            }
        }
    }
}
