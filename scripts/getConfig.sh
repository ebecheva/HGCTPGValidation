#!/bin/bash

# ./getConfig.sh subset_config_name label
 

echo "subset_config " $1
echo "label " $2

module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
module avail
module purge
module load python/3.9.9

python --version
python ../../../HGCTPGValidation/scripts/read_configuration_Jenkins.py --subsetconfig $1 --label $2



