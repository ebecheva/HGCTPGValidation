#!/usr/bin/env bash
# source ../HGCTPGValidation/scripts/extractReleaseName.sh $CHANGE_TARGET

# Important
# When this script is used in Groovy script, it is imperative to not use other echo messages
# except the last "echo -n "$REF_RELEASE"" message
# The "-n" option is mandatory in order to out result without a newline 

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
    #echo "===The name of the release is $s"
    export REF_RELEASE=$s
    break
  fi
  done
done
unset IFS
echo -n "$REF_RELEASE"

