pipeline {
    agent {
        label 'llrgrhgtrig.in2p3.fr'
    }
    environment {
        EMAIL_TO = 'becheva@llr.in2p3.fr'
        CONFIG_SUBSET = 'default_subset'
    }
    options {
        skipDefaultCheckout() 
    }
    stages {
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
                        export LABEL="test"
                        if [ -z "$CHANGE_FORK" ]
                        then
                            export REMOTE="ebecheva"
                        else
                            export REMOTE=$CHANGE_FORK
                        fi
                        echo 'REMOTE= ', $REMOTE
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $CHANGE_BRANCH $CHANGE_TARGET $LABEL
                        '''
                    }
                }
                stage('QualityChecks'){
                    steps{
                        sh '''
                        source /cvmfs/cms.cern.ch/cmsset_default.sh
                        source ./HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                        export LABEL="test"
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_$LABEL/src
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
                        export LABEL="test"
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_$LABEL/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        python ../../../HGCTPGValidation/scripts/produceData_from_configuration.py --subsetconfig ${CONFIG_SUBSET} --label $LABEL
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
                        export LABEL="ref"
                        export REMOTE="ebecheva"
                        ../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $CHANGE_TARGET $CHANGE_TARGET $LABEL
                        '''
                    }
                }           
                stage('Produce'){
                    steps {
                        sh '''
                        pwd
                        source ./HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET
                        export LABEL="ref"
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_$LABEL/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        python ../../../HGCTPGValidation/scripts/produceData_from_configuration.py --subsetconfig ${CONFIG_SUBSET} --label $LABEL
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
                ../HGCTPGValidation/scripts/displayHistos.sh ./${REF_RELEASE}_HGCalTPGValidation_ref/src ./${REF_RELEASE}_HGCalTPGValidation_test/src ./GIFS
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
