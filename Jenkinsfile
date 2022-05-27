pipeline {
    agent {
        label 'llrgrhgtrig.in2p3.fr'
    }
    environment {
        EMAIL_TO = 'jenkins@llr.in2p3.fr'
    }
    options {
        skipDefaultCheckout() 
    }
    stages {
        stage('InstallAutoValidationPackage') {
            steps {
                echo 'Building..'
                sh '''
                uname -a
                whoami
                pwd
                ls -l
                if [ -d "./HGCTPGValidation" ] 
                then
                    rm -rf HGCTPGValidation
                fi
                git clone -b Jenkins-developments https://github.com/hgc-tpg/HGCTPGValidation HGCTPGValidation
                ~/grid_login
                source HGCTPGValidation/env_install.sh
                pip install attrs
                if [ -d "./test_dir" ] 
                then
                    echo "Directory test_dir exists." 
                    rm -rf test_dir
                fi
                mkdir test_dir
                ls -lrt ..
                '''
            }
        }
        stage('BuildValidation'){
            failFast true
            parallel{
                stage('BuildCMSSWRef'){
                    stages{
                        stage('Install'){
                            steps {
                                echo 'InstallCMSSW Ref step..'
                                sh '''
                                pwd
                                ~/grid_login
                                cd test_dir
                                source ../HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                                unset IFS
                                export LABEL="ref"
                                ../HGCTPGValidation/scripts/installCMSSW.sh $REF_RELEASE $CHANGE_TARGET $LABEL
                                '''
                            }
                        }
                        stage('Produce'){
                            steps {
                                sh '''
                                pwd
                                ~/grid_login
                                source ./HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                                unset IFS
                                export LABEL="ref"
                                cd test_dir/${REF_RELEASE}_HGCalTPGValidation_$LABEL/src
                                ../../../HGCTPGValidation/scripts/produceData.sh $LABEL
                                '''            
                            }
                        }
                    }
                }
                stage('BuildCMSSWTest'){
                    stages{
                        stage('Install'){
                            steps {
                                echo 'InstallCMSSW Test step..'
                                sh '''
                                pwd
                                ~/grid_login
                                cd test_dir
                                source ../HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                                unset IFS
                                export LABEL="test"
                                ../HGCTPGValidation/scripts/installCMSSW.sh $REF_RELEASE $CHANGE_BRANCH $LABEL
                                '''
                            }
                        }
                        stage('Produce'){
                            steps {
                                sh '''
                                pwd
                                ~/grid_login
                                source ./HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                                unset IFS
                                export LABEL="test"
                                cd test_dir/${REF_RELEASE}_HGCalTPGValidation_$LABEL/src
                                ../../../HGCTPGValidation/scripts/produceData.sh $LABEL
                                '''            
                            }
                        }
                    }
                }
            }
        }
        stage('Display') {
            steps {
                sh '''
                cd test_dir
                source ../HGCTPGValidation/env_install.sh
                echo $PWD
                REF_RELEASE=$(echo $CHANGE_TARGET | cut -d'-' -f 3)
                ../HGCTPGValidation/scripts/displayHistos.sh ./${REF_RELEASE}_HGCalTPGValidation_ref/src ./${REF_RELEASE}_HGCalTPGValidation_test/src ./GIFS
                echo 'CHANGE_ID= ', $CHANGE_ID
                echo '$CHANGE_TITLE= ', $CHANGE_TITLE
                if [ -d /data/jenkins/workspace/validation_data/PR$CHANGE_ID ] 
                then
                    echo "Directory " PR$CHANGE_ID " exists." 
                    rm -rf /data/jenkins/workspace/validation_data/PR$CHANGE_ID
                fi
                export data_dir=/data/jenkins/workspace/validation_data
                mkdir $data_dir/PR$CHANGE_ID
                cp -rf GIFS/. $data_dir/PR$CHANGE_ID
                python ../HGCTPGValidation/scripts/writeToFile.py --dirname $data_dir/PR$CHANGE_ID --prnumber $CHANGE_ID --prtitle "PR$CHANGE_ID : $CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)"
                '''            
            }
        }
    }
    post {
        always {
            echo 'The job finished.'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job was run: ${currentBuild.fullDisplayName} was run.",
                 body:  "The Jenkins job was run. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} to view the results."
        }
        success {
            echo 'The job finished successfully.'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job succeded: ${currentBuild.fullDisplayName}",
                 body:  "The job finished successfully. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} to view the results."
        }
        unstable {
            echo 'The job is unstable :/'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job, status Unstable : ${currentBuild.fullDisplayName}",
                 body:  "Unit tests failed. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} to view the results."
        }
        failure {
            echo 'Job failed'
            mail to: "${EMAIL_TO}",
                 subject: "Failed Jenkins job: ${currentBuild.fullDisplayName}",
                 body: "The compilation or the build steps failed. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} to view the results."
        }
        changed {
            echo 'Things were different before...'
            mail to: "${EMAIL_TO}",
                 subject: "Status=Changed for Jenkins job: ${currentBuild.fullDisplayName}",
                 body: "Build status has changed. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} to view the results."    
        }
    }
}
