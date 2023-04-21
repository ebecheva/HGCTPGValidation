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

source /cvmfs/cms.cern.ch/cmsset_default.sh
echo $PWD
eval `scramv1 runtime -sh`
python ${WORKSPACE}/HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_TEST} --workspace ${WORKSPACE} --release ${REF_RELEASE}
