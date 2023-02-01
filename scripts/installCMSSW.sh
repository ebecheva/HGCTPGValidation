#!/bin/bash

# This code is to use with Jenkins jobs triggering on Github Pull Request in the repository https://github.com/hgc-tpg
# ./installCMSSW.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $BASE_REMOTE $CHANGE_BRANCH $CHANGE_TARGET ${LABEL_TEST}

# $1 SCRAM_ARCH
# $2 release name
# $3 remote name 
# $4 base remote name
# $5 branch name (corresponds to the branch containing the changes)
# $6 reference branch name (this is the target or base branch to which the change could be merged, it is in https://github.com/hgc-tpg repository)
# $7 label "ref" or "test"

export SCRAM_ARCH=$1
echo $SCRAM_ARCH
relversion=$2
echo $relversion
remote=$3
echo $remote
baseremote=$4
echo $baseremote
branch=$5
echo $branch
branch_ref=$6
echo $branch_ref
label=$7
echo $label

source /cvmfs/cms.cern.ch/cmsset_default.sh
module purge
scramv1 p -n ${relversion}_HGCalTPGValidation_$label CMSSW $relversion
cd ${relversion}_HGCalTPGValidation_$label/src
echo $PWD
eval `scramv1 runtime -sh`
git cms-merge-topic $remote:$branch
git checkout -b local_$branch $remote/$branch
git cms-merge-topic $baseremote:$branch_ref
scram b -j8
