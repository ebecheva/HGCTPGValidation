#!/bin/bash

# ./getConfig.sh subset_config_name

# $1 label "ref" or "test"
# $2 procModifier 

echo "subset_config " $1
echo "label " $2

module purge
module load python/3.9.9
python --version
python ../../read_configuration_Jenkins_v4.py --subsetconfig $1 --label $2
echo '!!!!!!!!! 1 nbEvents= ' $nbEvents
