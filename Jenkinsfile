pipeline {
    agent {
        label 'llrgrhgtrig.in2p3.fr'
    }
    environment {
        LABEL_TEST='test'
        LABEL_REF='ref'
    }
    options {
        skipDefaultCheckout() 
    }
    stages {
        stage('SetEnvVar'){
            steps{
                script{
                    String s = env.JOB_NAME
                    s = s.substring(s.indexOf("/") + 1)
                    s = s.substring(0, s.indexOf("/"));
                    println(s);
                    switch(s){
                        case 'HGC TPG Automatic Validation':
                            env.EMAIL_TO=env.EMAIL_TO_MAIN
                            env.BASE_REMOTE=env.BASE_REMOTE_MAIN
                            env.DATA_DIR=env.DATA_DIR_MAIN
                            env.BRANCH_VAL=env.BRANCH_VAL_MAIN
                            break
                        case 'HGC TPG Automatic Validation - TEST':
                            env.EMAIL_TO=env.EMAIL_TO_EB
                            env.BASE_REMOTE=env.BASE_REMOTE_TEST
                            env.DATA_DIR=env.DATA_DIR_TEST
                            env.BRANCH_VAL=env.BRANCH_VAL_TEST
                            break
                        case 'HGC TPG Automatic Validation - TEST ebecheva':
                            env.EMAIL_TO=env.EMAIL_TO_EB
                            env.BASE_REMOTE=env.BASE_REMOTE_EB
                            env.DATA_DIR=env.DATA_DIR_EB
                            env.BRANCH_VAL=env.BRANCH_VAL_EB
                            break
                        case 'Job HGC TPG Automatic Validation - TEST jbsauvan':
                            env.EMAIL_TO=env.EMAIL_TO_JB
                            env.BASE_REMOTE=env.BASE_REMOTE_JB
                            env.DATA_DIR=env.DATA_DIR_JB
                            env.BRANCH_VAL=env.BRANCH_VAL_JB
                            break
                    }
                    println(env.BASE_REMOTE)
                    println(env.DATA_DIR)
                    println(env.BRANCH_VAL)
                }
            }  
        }
        stage('Initialize'){
            stages{
                stage('CleanEnv'){
                    steps{
                        echo 'Clean the working environment.'
                        sh '''
                        if [ -d "/data/jenkins/workspace/${DATA_DIR}/PR$CHANGE_ID" ]
                        then
                            rm -rf /data/jenkins/workspace/${DATA_DIR}/PR$CHANGE_ID
                        fi
                        '''
                    }
                }
                stage('InstallAutoValidationPackage') {
                    steps {
                        echo 'Install automatic validation package HGCTPGValidation.'
                        sh '''
                        uname -a
                        whoami
                        pwd
                        ls -l
                        if [ -d "./HGCTPGValidation" ] 
                        then
                            rm -rf HGCTPGValidation
                        fi
                        git clone -b ${BRANCH_VAL} https://github.com/${BASE_REMOTE}/HGCTPGValidation HGCTPGValidation
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
            }
        }
        stage('BuildCMSSWTest'){
            stages{
                stage('Install'){
                    steps {
                        echo 'InstallCMSSW Test step..'
                        sh '''
                        pwd
                        cd test_dir
                        source ../HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                        source ../HGCTPGValidation/scripts/getScramArch.sh $REF_RELEASE
                        if [ -z "$CHANGE_FORK" ]
                        then
                            export REMOTE=$BASE_REMOTE
                        else
                            export REMOTE=$CHANGE_FORK
                        fi
                        echo 'REMOTE= ', $REMOTE
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $BASE_REMOTE $CHANGE_BRANCH $CHANGE_TARGET ${LABEL_TEST}
                        '''
                    }
                }
                stage('QualityChecks'){
                    steps{
                        sh '''
                        source /cvmfs/cms.cern.ch/cmsset_default.sh
                        source ./HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
                        scram build code-checks
                        scram build code-format
                        GIT_STATUS=`git status --porcelain`
                        if [ ! -z "$GIT_STATUS" ]; then
                            echo "Code-checks or code-format failed."
                            exit 1;
                        fi
                        '''
                    }
                }
                stage('Produce'){
                    steps {
                        sh '''
                        pwd
                        source ./HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                        export PROC_MODIFIER=""
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
                        ../../../HGCTPGValidation/scripts/produceData.sh ${LABEL_TEST} $PROC_MODIFIER
                        '''            
                    }
                }
            }
        }
        stage('BuildCMSSWRef'){
            stages{
                stage('Install'){
                    steps {
                        echo 'InstallCMSSW Ref step..'
                        sh '''
                        pwd
                        cd test_dir
                        source ../HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                        source ../HGCTPGValidation/scripts/getScramArch.sh $REF_RELEASE
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $BASE_REMOTE $BASE_REMOTE $CHANGE_TARGET $CHANGE_TARGET ${LABEL_REF}
                        '''
                    }
                }           
                stage('Produce'){
                    steps {
                        sh '''
                        pwd
                        source ./HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                        export PROC_MODIFIER=""
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src
                        ../../../HGCTPGValidation/scripts/produceData.sh ${LABEL_REF} $PROC_MODIFIER
                        '''            
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
                source ../HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                ../HGCTPGValidation/scripts/displayHistos.sh ./${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src ./${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src ./GIFS
                echo 'CHANGE_ID= ', $CHANGE_ID
                echo '$CHANGE_TITLE= ', $CHANGE_TITLE
                if [ -d /data/jenkins/workspace/${DATA_DIR}/PR$CHANGE_ID ] 
                then
                    echo "Directory " PR$CHANGE_ID " exists." 
                    rm -rf /data/jenkins/workspace/${DATA_DIR}/PR$CHANGE_ID
                fi
                export data_dir=/data/jenkins/workspace/${DATA_DIR}
                mkdir $data_dir/PR$CHANGE_ID
                mkdir $data_dir/PR$CHANGE_ID/"PR$CHANGE_ID"config1
                cp -rf GIFS/. $data_dir/PR$CHANGE_ID/"PR$CHANGE_ID"config1
                python ../HGCTPGValidation/scripts/writeToFile.py --dirname $data_dir/PR$CHANGE_ID --prnumber $CHANGE_ID --prtitle "$CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)"
                '''            
            }
        }
    }
    post {
        success {
            echo 'The job finished successfully.'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job succeded: ${currentBuild.fullDisplayName}",
                 body:  "The job finished successfully. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} \n\n and ${env.CHANGE_URL} to view the results.  \n\n The validation histograms are available at https://llrhgcaltpgvalidation.in2p3.fr/PR/ \n\n"
        }
        failure {
            echo 'Job failed'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job failed: ${currentBuild.fullDisplayName}",
                 body: "The compilation or the build steps failed. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} \n\n and ${env.CHANGE_URL} to view the results.  \n\n The validation histograms are available at https://llrhgcaltpgvalidation.in2p3.fr/PR/ \n\n"
        }
    }
}
