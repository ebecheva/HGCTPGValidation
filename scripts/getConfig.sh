#!/bin/bash

# ./getConfig.sh subset_config_name

# $1 label "ref" or "test"
# $2 procModifier 

echo "subset_config " $1
echo "label " $2

#module purge
#module load python/3.7.0
source /cvmfs/cms.cern.ch/cmsset_default.sh
python --version
python ./read_configuration_Jenkins.py --subsetconfig $1 --label $2

