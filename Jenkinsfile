pipeline {
    agent {
        label 'llrgrhgtrig.in2p3.fr'
    }
    environment {
        LABEL_TEST='test'
        LABEL_REF='ref'
        CONFIG_SUBSET = 'default_multi_subset'
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
                    println(env.CHANGE_TARGET)
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
                stage('SetCMSSWEnvVar'){
                    steps{
                        script{
                            VAR_REL = sh(returnStdout: true, script: 'source ./HGCTPGValidation/scripts/extractReleaseName.sh ${CHANGE_TARGET}')
                            env.REF_RELEASE=VAR_REL
                            println(env.REF_RELEASE)
                            VAR_SCRAM_ARCH = sh(returnStdout: true, script: 'source ./HGCTPGValidation/scripts/getScramArch_EnvVar.sh ${REF_RELEASE}')
                            env.SCRAM_ARCH=VAR_SCRAM_ARCH
                            println(env.SCRAM_ARCH)
                        }
                        echo "REF_RELEASE= ${REF_RELEASE}"
                        echo "SCRAM_ARCH = ${SCRAM_ARCH}"
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
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        echo ' CONFIG_SUBSET = ' ${CONFIG_SUBSET}
                        echo 'LABEL_TEST = ' ${LABEL_TEST}
                        python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_TEST}
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
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $BASE_REMOTE $BASE_REMOTE $CHANGE_TARGET $CHANGE_TARGET ${LABEL_REF}
                        '''
                    }
                }           
                stage('Produce'){
                    steps {
                        sh '''
                        pwd
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        echo ' CONFIG_SUBSET = ' ${CONFIG_SUBSET}
                        python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_REF}
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
                python ../HGCTPGValidation/scripts/displayHistos.py --subsetconfig ${CONFIG_SUBSET} --refdir ${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src --testdir ${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src --datadir ${DATA_DIR} --prnumber $CHANGE_ID --prtitle "$CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)"
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
