#!/bin/bash

# Set environment variables used for the standalone validation


# Variables to modify by the user ############################

# CMSSW
export SCRAM_ARCH='slc7_amd64_gcc10'
echo $SCRAM_ARCH

export REF_RELEASE='CMSSW_12_5_2_patch1'
echo $REF_RELEASE

export BASE_REMOTE='hgc-tpg'
echo $BASE_REMOTE

export REMOTE='hgc-tpg'
echo $REMOTE

export CHANGE_BRANCH='hgc-tpg-CMSSW_12_5_2_patch1'
echo $CHANGE_BRANCH

export CHANGE_TARGET='hgc-tpg-CMSSW_12_5_2_patch1'
echo $CHANGE_TARGET

CONFIG_SUBSET='default_multi_subset'
export $CONFIG_SUBSET
echo $CONFIG_SUBSET

# Variables relative to the generated data
export CHANGE_ID='01'
export WEBPAGE_TITLE='Standalone validation'

#################################################

# Fixed variables
export LABEL_TEST='test'
echo $LABEL_TEST

export LABEL_REF='ref'
echo $LABEL_REF

export DATA_DIR='.'
