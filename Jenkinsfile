pipeline {
    agent {
        label 'llrgrhgtrig.in2p3.fr'
    }
    environment {
        EMAIL_TO = 'becheva@llr.in2p3.fr'
        LABEL_TEST='test'
        LABEL_REF='ref'
        CONFIG_SUBSET = 'default_subset'
    }
    options {
        skipDefaultCheckout() 
    }
    stages {
        stage('SetEnvVar'){
            steps{
                sh'''
                echo 'RewriteEnvVar stage'
                echo 'LABEL_TEST ' ${LABEL_TEST}
                echo 'EMAIL_TO = ' ${EMAIL_TO}
                echo 'CONFIG_SUBSET =' ${CONFIG_SUBSET}
                echo 'Job base name = ' ${JOB_BASE_NAME}
                echo 'Job name = ' ${JOB_NAME}
                JENKINS_JOB_NAME=$(echo ${JOB_NAME} | cut -d'/' -f 2)
                echo 'The job name is: ' $JENKINS_JOB_NAME
                '''
                script{
                    switch('${env.JENKINS_JOB_NAME}'){
                        case 'HGC TPG Automatic Validation':
                            env.EMAIL_TO='jenkins@llr.in2p3.fr'
                            env.BASE_REMOTE='hgc-tpg'
                            env.DATA_DIR='validation_data'
                            env.BRANCH_VAL='master'
                        case 'HGC TPG Automatic Validation - TEST':
                            env.EMAIL_TO='becheva@llr.in2p3.fr'
                            env.BASE_REMOTE='hgc-tpg'
                            env.DATA_DIR='validation_data_test'
                            env.BRANCH_VAL='Jenkins-developments-test'
                        case 'HGC TPG Automatic Validation - TEST ebecheva':
                            env.EMAIL_TO='emilia.becheva@llr.in2p3.fr'
                            env.BASE_REMOTE='ebecheva'
                            env.DATA_DIR='validation_data_test_emilia'
                            env.BRANCH_VAL='Jenkins-newFeature_readMulticonfig'
                    }
                }
                sh'''
                echo 'Selected email address ${env.EMAIL_TO}'
                echo 'BASE_REMOTE = ${env.BASE_REMOTE}'
                echo 'DATA_DIR = ${env.DATA_DIR}'
                echo 'BRANCH_VAL = ${env.BRANCH_VAL}'
               '''
            }   
        }
        stage('Initialize'){
            stages{
                stage('CleanEnv'){
                    steps{
                        echo 'Clean the working environment.'
                        sh '''
                        if [ -d "/data/jenkins/workspace/validation_data_test_emilia//PR$CHANGE_ID" ] 
                        then
                            rm -rf /data/jenkins/workspace/validation_data_test_emilia//PR$CHANGE_ID
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
                        git clone -b Jenkins-newFeature_readMulticonfig https://github.com/ebecheva/HGCTPGValidation HGCTPGValidation
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
                            export REMOTE="ebecheva"
                        else
                            export REMOTE=$CHANGE_FORK
                        fi
                        echo 'REMOTE= ', $REMOTE
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $CHANGE_BRANCH $CHANGE_TARGET ${LABEL_TEST}
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
                        #export LABEL="test"
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        echo ' CONFIG_SUBSET = ' ${CONFIG_SUBSET}
                        echo 'LABEL_TEST = ' ${LABEL_TEST}
                        python ../../../HGCTPGValidation/scripts/produceData_from_configuration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_TEST}
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
                        export REMOTE="ebecheva"
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $CHANGE_TARGET $CHANGE_TARGET ${LABEL_REF}
                        '''
                    }
                }           
                stage('Produce'){
                    steps {
                        sh '''
                        pwd
                        source ./HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                        #export LABEL="ref"
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        echo ' CONFIG_SUBSET = ' ${CONFIG_SUBSET}
                        python ../../../HGCTPGValidation/scripts/produceData_from_configuration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_REF}
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
                if [ -d /data/jenkins/workspace/validation_data_test_emilia//PR$CHANGE_ID ] 
                then
                    echo "Directory " PR$CHANGE_ID " exists." 
                    rm -rf /data/jenkins/workspace/validation_data_test_emilia//PR$CHANGE_ID
                fi
                export data_dir=/data/jenkins/workspace/validation_data_test_emilia/
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
