#!/bin/bash

## STANDALONE VALIDATION
## The script is similar to the Jenkins pipeline
## To runs the standalne validation:
## 1. Install the validation package from the relevant branch
## mkdir validation/
## cd validation/
## git clone -b ${BRANCH_HGCTPGVAL} https://github.com/${REMOTE_HGCTPGVAL}/HGCTPGValidation HGCTPGValidation
## source HGCTPGValidation/env_install.sh
## 2. The needs to adapt the variables in HGCTPGValidation/config/user.envvar.sh
## 3. ./HGCTPGValidation/scripts/standalone_hgctpg_validation.sh
##
## The validation repositories are organized as follows
## ./validation/HGCTPGValidation/
## ./validation/test_dir/
## ./validation/test_dir/CMSSW_...
## ./validation/test_dir/CMSSW...
## ./PR00
## The generated webpages and the pictures are stored in a repository at the same level as validation/. 
## The name of the results repository is set in the HGCTPGValidation/config/user.envvar.sh file


uname -a
whoami
pwd

if [ -d "./test_dir" ] 
then
    echo "Directory test_dir exists."
    rm -rf test_dir
fi

mkdir test_dir
cd test_dir

source ../HGCTPGValidation/config/user_envvar.sh

echo 'Install automatic validation package HGCTPGValidation.'


#BuildCMSSWTest -----------------------------------
## Install
../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $BASE_REMOTE $CHANGE_BRANCH $CHANGE_TARGET $LABEL_TEST

## QualityChecks
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
scram build code-checks
scram build code-format
GIT_STATUS=`git status --porcelain`
if [ ! -z "$GIT_STATUS" ]; 
then
    echo "Code-checks or code-format failed."
    exit 1;
fi

## Produce
module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
module purge
module load python/3.9.9
python --version

python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label $LABEL_TEST
cd ../..
#------------------------------------------------

#BuildCMSSWRef ---------------------------------
pwd
## Install
../HGCTPGValidation/scripts/installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $BASE_REMOTE $BASE_REMOTE $CHANGE_TARGET $CHANGE_TARGET $LABEL_REF

## Produce
pwd
cd ${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src
module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
module purge
module load python/3.9.9
python --version
python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label $LABEL_REF
cd ../..
#-----------------------------------------------


# Display
pwd
source ../HGCTPGValidation/env_install.sh
python ../HGCTPGValidation/scripts/displayHistos.py --subsetconfig ${CONFIG_SUBSET} --refdir ${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src --testdir ${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src --datadir ${DATA_DIR} --prnumber 00 --prtitle ${WEBPAGE_TITLE}

