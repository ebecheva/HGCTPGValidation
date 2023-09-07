#!/usr/bin/env bash
# $1 CMSSW release version
# source ../HGCTPGValidation/scripts/getScramArch.sh $REF_RELEASE
# For example
# ./getScramArch.sh CMSSW_12_2_0
# scram list -c $1 gives the following result
#CMSSW           CMSSW_12_2_0              /cvmfs/cms.cern.ch/slc7_amd64_gcc10/cms/cmssw/CMSSW_12_2_0
#CMSSW           CMSSW_12_2_0              /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0

# The program extracts the scram_arch for the more recent gcc version (if there more than one arches)

# This script is used in a Groovy script in Jenkinsfile. 
# The information from thelast line of the script, "echo $SCRAM_ARCH", is written in the stdout 
# that is taken to fill the global variable SCRAM_ARCH in Jenkinsfile.
# For this reason, it is imperative to not add other "echo" messages except the last one.

# Show available SCRAM-based projects for selected SCRAM_ARCH. 
source /cvmfs/cms.cern.ch/cmsset_default.sh

# Use scram list and grep to select the lines corresponding to 
# the CMSSW release version we want to use
# scram list -c display the result in a simple lines, 
# grep -w show the lines that match exactly to the release name 
# for ex. we'll see the lines only for CMSSW_12_2_0, not for the pre-releases

scram list -c $1  | grep -w $1 > out
input="out"
declare -i i=0
#create an array to store gcc versions
final_gcc_version=()
scram_arch_array=()
# read the file containing the  
while IFS= read -r line
do
  # Get the second part that corresponds to the name of the release
  REL_NAME=$(echo $line | cut -d' ' -f 2)
  if [ "$REL_NAME" =  "$1" ]
  then
    # Get the last part of each line read in the file
    SUBSTR=$(echo $line | cut -d' ' -f 3)
    # Extract the scram_arch name
    scram_arch=$(echo $SUBSTR | cut -d'/' -f 4)
    scram_arch_array[$i]=$scram_arch
    # Extract the gcc name version, ex gcc900, or gcc10
    gcc=$(echo $scram_arch| cut -d'_' -f 3)
    # Extract the gcc version from the name of the version, ex "10" 
    version=${gcc:3}
    # Get the length of "version"
    length=$((${#version}))
    # slc7_amd64_gcc11, or slc7_amd64_gcc10, slc7_amd64_gcc900....
    if [ "$length" -le 2 ]
    then
      v=$(( version*100 ))
      final_gcc_version[$i]=$v
    else
      final_gcc_version[$i]=$version
    fi
    j=$((i-1))
    # Compare the current version with the previous one
    # Keep the latest version
    if [[ "$i" -ne 0 ]] && [[ ${final_gcc_version[$i]} -gt  ${final_gcc_version[$((i-1))]} ]]
    then
      recent_gcc_version=${final_gcc_version[$i]}
      SCRAM_ARCH=${scram_arch_array[$i]}
    else
      recent_gcc_version=${final_gcc_version[$((i-1))]}
      SCRAM_ARCH=${scram_arch_array[$i-1]}
    fi
    export $SCRAM_ARCH
  fi
  ((i=i+1))
done < "$input"
# The printed SCRAM_ARCH value is used to fill the global variable SCRAM_ARCH in Jenkinsfile
# Please, see the detailed information at the beginning of this file.
echo -n $SCRAM_ARCH
