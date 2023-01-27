#!/usr/bin/env bash

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
echo "$REF_RELEASE"

