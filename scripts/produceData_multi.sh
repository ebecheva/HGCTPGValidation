#!/bin/bash

# ./produceData_multi.sh ${CONFIG_SUBSET} ${LABEL_TEST} ${WORKSPACE} ${REF_RELEASE}

# $1 CONFIG_SUBSET
# $2 procModifier
# $3 label => test or ref 
# $4 release: CMSSW_X_Y_Z 

echo "Config_subset = " $1
echo "Label = " $2
echo "Workspace dir = " $3
echo "Release = " $4

set -v
pwd
cd ${WORKSPACE}/test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
source /cvmfs/cms.cern.ch/cmsset_default.sh
module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
module purge
module load python/3.9.9
python --version
python $3/HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig $1 --label $2 --workspace $3 --release $4
