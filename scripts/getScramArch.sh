#!/usr/bin/env bash
# $1 CMSSW release version
# source ../HGCTPGValidation/scripts/getScramArch.sh $REF_RELEASE
# For example
# ./getScramArch.sh CMSSW_12_2_0
# scram list -c $1 gives the following result
#CMSSW           CMSSW_12_2_0              /cvmfs/cms.cern.ch/slc7_amd64_gcc10/cms/cmssw/CMSSW_12_2_0
#CMSSW           CMSSW_12_2_0              /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0

# The program extracts the scram_arch for the more recent gcc version (if there more than one arches)
# When using this script inside a Groovy script, do not add other "echo.." messages except the last one

# Show available SCRAM-based projects for selected SCRAM_ARCH. 
source /cvmfs/cms.cern.ch/cmsset_default.sh

# Use scram list and grep to select the lines corresponding to 
# the CMSSW release version we want to use
# scram list -c display the result in a simple lines, 
# grep -w show the lines that match exactly to the release name 
# for ex. we'll see the lines only for CMSSW_12_2_0, not for the pre-releases
#echo "Release to use = " $1
scram list -c $1  | grep -w $1 > out
input="out"
declare -i i=0
#create an array to store gcc versions
final_gcc_version=()
scram_arch_array=()
# read the file containing the  
while IFS= read -r line
do
  #echo i: $i
  #echo "my line: $line"
  # Get the second part that corresponds to the name of the release
  REL_NAME=$(echo $line | cut -d' ' -f 2)
  if [ "$REL_NAME" =  "$1" ]
  then
    #echo " REL_NAME = " $REL_NAME
    # Get the last part of each line read in the file
    SUBSTR=$(echo $line | cut -d' ' -f 3)
    #echo " sub= " $SUBSTR
    # Extract the scram_arch name
    scram_arch=$(echo $SUBSTR | cut -d'/' -f 4)
    scram_arch_array[$i]=$scram_arch
    #echo " scram_arch = " ${scram_arch_array[$i]}
    # Extract the gcc name version, ex gcc900, or gcc10
    gcc=$(echo $scram_arch| cut -d'_' -f 3)
    #echo " gcc name version = " $gcc
    # Extract the gcc version from the name of the version, ex "10" 
    version=${gcc:3}
    #echo " legth of the version name = " ${#version}
    # Get the length of "version"
    length=$((${#version}))
    #echo $length
    # slc7_amd64_gcc11, or slc7_amd64_gcc10, slc7_amd64_gcc900....
    if [ "$length" -le 2 ]
    then
      v=$(( version*100 ))
      final_gcc_version[$i]=$v
    else
      final_gcc_version[$i]=$version
    fi
    #echo " gcc version = " ${final_gcc_version[$i]}
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
    #echo "the most recent gcc version is (x100) = " $recent_gcc_version
    #echo "the scram_arch to use is = " $SCRAM_ARCH
  fi
  ((i=i+1))
done < "$input"
echo $SCRAM_ARCH
