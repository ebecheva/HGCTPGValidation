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
        stage('Set environment variables'){
            steps{
                sh '''
                set +x
                echo '==> Set environment variables'
                exec >> log_Jenkins
                if [ -f "log_Jenkins" ]; then
                    echo "Remove the last created log_Jenkins."
                    rm log_Jenkins
                else 
                    echo "log_Jenkins does not exist."
                fi 
                echo '==> Set environment variables'
                '''
                script{
                    String s = env.JOB_NAME
                    String[] elements = s.split("/")
                    String job_name = elements[-2]
                    println(job_name);
                    switch(job_name){
                       case 'HGC TPG CMSSW Validation':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_MAIN
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_MAIN
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_MAIN
                            env.BRANCH_HGCTPGVAL=env.HGCTPG_BRANCH_VAL_MAIN
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_PROD
                            env.JOB_FLAG=0
                            break
                        case 'HGC TPG Automatic Validation - TEST':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_EB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_TEST
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_TEST
                            env.BRANCH_HGCTPGVAL=env.HGCTPG_BRANCH_VAL_TEST
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST
                            env.JOB_FLAG=0
                            break
                        case 'HGC TPG Automatic Validation - TEST ebecheva':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_EB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_EB
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_EB
                            env.BRANCH_HGCTPGVAL=env.HGCTPG_BRANCH_VAL_EB
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST_EB
                            env.JOB_FLAG=0
                            break
                        case 'HGC TPG Automatic Validation - TEST jbsauvan':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_JB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_JB
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_JB
                            env.BRANCH_HGCTPGVAL=env.HGCTPG_BRANCH_VAL_JB
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST_JB
                            env.JOB_FLAG=0
                            break
                        case 'HGC TPG Validation Validation':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_MAIN
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_MAIN
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_VALTEST
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CODE_TEST
                            env.JOB_FLAG=1
                            break
                        case 'HGC TPG Dev Validation - ebecheva':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_EB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_EB
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_EB
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST_EB
                            env.JOB_FLAG=1
                            break
                        default: 
                            println("The job name is unknown"); 
                            break
                    }
                    
                    if (env.JOB_FLAG=='1'){
                        
                        env.BRANCH_HGCTPGVAL=env.CHANGE_BRANCH
                        env.CHANGE_TARGET_HGCTPGVAL=env.CHANGE_TARGET
                        
                        if (env.CHANGE_FORK){
                            env.REMOTE_HGCTPGVAL = env.CHANGE_FORK
                        }
                        else {
                            env.REMOTE_HGCTPGVAL = env.BASE_REMOTE
                        }
                    }
                    
                    println(env.REMOTE_HGCTPGVAL)
                    println(env.BRANCH_HGCTPGVAL)
                    
                    
                    println(env.BASE_REMOTE)
                    println(env.DATA_DIR)
                    println(env.CHANGE_TARGET)
                    println(env.CHANGE_BRANCH)
                    println(env.CHANGE_URL)
                    println(env.CHANGE_FORK)
                }
            }  
        }
        stage('Initialize'){
            stages{
                stage('Clean the working environment'){
                    steps{
                        sh '''
                        set +x
                        echo '==> Clean the working environment. ============================'
                        exec >> log_Jenkins
                        echo '==> Clean the working environment. ============================'
                        if [ -d "/data/jenkins/workspace/${DATA_DIR}/PR$CHANGE_ID" ]
                        then
                            rm -rf /data/jenkins/workspace/${DATA_DIR}/PR$CHANGE_ID
                        fi
                        echo '   '
                        '''
                    }
                }
                stage('Install automatic validation package HGCTPGValidation') {
                    steps {
                        sh '''
                        set +x
                        echo '==> Install automatic validation package HGCTPGValidation. ============================'
                        exec >> log_Jenkins
                        echo '==> Install automatic validation package HGCTPGValidation. ============================'
                        uname -a
                        whoami
                        pwd
                        ls -l
                        if [ -d "./HGCTPGValidation" ] 
                        then
                            rm -rf HGCTPGValidation
                        fi
                        git clone -b ${BRANCH_HGCTPGVAL} https://github.com/${REMOTE_HGCTPGVAL}/HGCTPGValidation HGCTPGValidation
                        source HGCTPGValidation/env_install.sh
                        pip install attrs
                        if [ -d "./test_dir" ] 
                        then
                            echo "Directory test_dir exists."
                            rm -rf test_dir
                        fi
                        mkdir test_dir
                        ls -lrt ..
                        echo '   '
                        '''
                    }
                }
                stage('Set CMSSW environment variables'){
                    steps{
                        script{
                            sh '''
                            set +x
                            echo 'echo ==> Set CMSSW environment variables. ============================'
                            exec >> log_Jenkins
                            echo 'echo ==> Set CMSSW environment variables. ============================'
                            '''
                            if ( env.JOB_FLAG == '0' ){
                                env.REF_RELEASE = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; source ./HGCTPGValidation/scripts/extractReleaseName.sh ${CHANGE_TARGET}').trim()
                                env.SCRAM_ARCH = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; source ./HGCTPGValidation/scripts/getScramArch.sh ${REF_RELEASE}').trim()
                                
                                if (env.CHANGE_FORK){
                                    env.REMOTE = env.CHANGE_FORK
                                }
                                else {
                                    env.REMOTE = env.BASE_REMOTE
                                }
                                
                                println(env.REF_RELEASE)
                                println(env.SCRAM_ARCH)
                                println(env.REMOTE)
                            } 
                            else {
                                env.REF_BRANCH = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/; module purge; module load python/3.9.9; python ./HGCTPGValidation/scripts/get_cmsswRefBranch.py').trim()
                                env.REF_RELEASE = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; source ./HGCTPGValidation/scripts/extractReleaseName.sh ${REF_BRANCH}').trim()
                                env.SCRAM_ARCH = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; source ./HGCTPGValidation/scripts/getScramArch.sh ${REF_RELEASE}').trim()
                                env.BASE_REMOTE = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/; module purge; module load python/3.9.9; python ./HGCTPGValidation/scripts/get_remoteParam.py').trim()
                                env.CHANGE_BRANCH = env.REF_BRANCH
                                env.CHANGE_TARGET = env.REF_BRANCH
                                env.REMOTE = env.BASE_REMOTE

                                println(env.REF_BRANCH)
                                println(env.REF_RELEASE)
                                println(env.SCRAM_ARCH)
                                println(env.BASE_REMOTE)
                                println(env.REMOTE)
                            }
                        }
                        sh '''
                        set +x
                        exec >> log_Jenkins
                        echo '  '
                        '''
                    }
                }
            }
        }
        stage('Build CMSSW Test release'){
            stages{
                stage('Install'){
                    steps {
                        sh '''
                        set +x
                        echo '==> Build CMSSW Test ========================='
                        echo '===> InstallCMSSW Test Step'
                        exec >> log_Jenkins
                        echo '==> Build CMSSW Test ========================='
                        echo '===> InstallCMSSW Test Step'
                        pwd
                        cd test_dir
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $BASE_REMOTE $CHANGE_BRANCH $CHANGE_TARGET ${LABEL_TEST}
                        echo '     '
                        '''
                    }
                }
                stage('Quality Checks'){
                    steps{
                        sh '''
                        set +x
                        echo '===> Quality checks'
                        exec >> log_Jenkins
                        echo '===> Quality checks'
                        source /cvmfs/cms.cern.ch/cmsset_default.sh
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
                        scram build code-checks
                        scram build code-format
                        GIT_STATUS=`git status --porcelain`
                        if [ ! -z "$GIT_STATUS" ]; then
                            echo "Code-checks or code-format failed."
                            exit 1;
                        fi
                        echo '    '
                        '''
                    }
                }
                stage('Produce'){
                       steps {
                        script{
                        sh '''
                        set +x
                        echo '===> Produce test data.'
                        exec >> log_Jenkins
                        echo '===> Produce test data.'
                        pwd
                        '''
                        env.EXIT_CODE_PRODUCE = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src; module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/; module purge; module load python/3.9.9; python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_TEST}').trim()
                        println(env.EXIT_CODE_PRODUCE)
                            
                        }
                        sh '''
                       
                        echo 'EXIT_CODE_PRODUCE=' $EXIT_CODE_PRODUCE
                        '''
                    }
                }
            }
        }
        stage('Build CMSSW Ref release'){
            stages{
                stage('Install'){
                    steps {
                        sh '''
                        set +x
                        echo '==> Build CMSSW Reference ======================='
                        echo '===> InstallCMSSW Ref'
                        exec >> log_Jenkins
                        echo '==> Build CMSSW Reference ======================='
                        echo '===> InstallCMSSW Ref'
                        pwd
                        cd test_dir
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $BASE_REMOTE $BASE_REMOTE $CHANGE_TARGET $CHANGE_TARGET ${LABEL_REF}
                        echo '      '
                        '''
                    }
                }           
                stage('Produce'){
                    steps {
                        sh '''
                        set +x
                        echo '===> Produce reference data.'
                        exec >> log_Jenkins
                        echo '===> Produce reference data.'
                        pwd
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        echo ' CONFIG_SUBSET = ' ${CONFIG_SUBSET}
                        python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_REF}
                        echo '      '
                        '''
                    }
                }
            }
        }
        stage('Display') {
            steps {
                sh '''
                set +x
                echo '==> Display ======================='
                exec >> log_Jenkins
                echo '==> Display ======================='
                cd test_dir
                source ../HGCTPGValidation/env_install.sh
                echo $PWD
                python ../HGCTPGValidation/scripts/displayHistos.py --subsetconfig ${CONFIG_SUBSET} --refdir ${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src --testdir ${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src --datadir ${DATA_DIR} --prnumber $CHANGE_ID --prtitle "$CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)"
                echo '      '
                '''
            }
        }
    }
    post {
        always {
            script{
                if ( env.JOB_FLAG=='1' ) {    
                    env.CHANGE_BRANCH = env.BRANCH_HGCTPGVAL
                    env.CHANGE_TARGET = env.CHANGE_TARGET_HGCTPGVAL
                    println( "Validation of the validation: Set the original name of CHANGE_BRANCH => " + env.CHANGE_BRANCH )
                }
            }
            archiveArtifacts artifacts: 'log_Jenkins', fingerprint: true
        }
        success {
            echo 'The job finished successfully.'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job succeded: ${currentBuild.fullDisplayName}",
                 body:  "The job finished successfully. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} \n\n and ${env.CHANGE_URL} to view the results.  \n\n The validation histograms are available at ${env.WEBPAGES_VAL} \n\n"
        }
        failure {
            echo 'Job failed'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job failed: ${currentBuild.fullDisplayName}",
                 body: "The compilation or the build steps failed. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} \n\n and ${env.CHANGE_URL} to view the results.  \n\n The validation histograms are available at ${env.WEBPAGES_VAL} \n\n"
        }
    }
}
