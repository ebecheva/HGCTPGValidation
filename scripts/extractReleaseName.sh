#!/usr/bin/env bash
# source ../HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET

# This script extract the release name from the name of the target branch
#
# Important
# This script is used in a Groovy script in Jenkinsfile.
# The information from the last line of the script, "echo -n "$REF_RELEASE"", is written in the stdout
# then is used to fill the global variable REF_RELEASE in Jenkinsfile.
# For this reason, it is imperative to not add other "echo" messages except this last one.
# The "-n" option is mandatory, it allows to out the result without a newline.

########################################################
IFS="-"
for i in $1
do
  s=$i
  IFS="_"
  for j in $s
  do
    rel=$j
    if [ "$rel" == "CMSSW" ]
    then
    export REF_RELEASE=$s
    break
  fi
  done
done
unset IFS
echo -n "$REF_RELEASE"

