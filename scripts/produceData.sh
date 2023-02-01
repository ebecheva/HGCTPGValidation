#!/bin/bash

# ./produceData.sh $LABEL $PROC_MODIFIER

# $1 label "ref" or "test"
# $2 procModifier 

echo "label " $1
echo "procModifiers " $2

source /cvmfs/cms.cern.ch/cmsset_default.sh
echo $PWD
eval `scramv1 runtime -sh`
if [[ -n $2 ]] #if not empty
then
  cmsDriver.py hgcal_tpg_validation -n 50 + \
  --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW + \
  --conditions auto:phase2_realistic_T15 + \
  --beamspot HLLHC14TeV + \
  --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation + \
  --geometry Extended2026D49 --era Phase2C9 --procModifiers $2 + \
  --inputCommands "keep *","drop l1tTkPrimaryVertexs_L1TkPrimaryVertex__RECO" + \
  --filein file:/data_CMS_upgrade/data_jenkins/Phase2HLTTDRSummer20ReRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v2/003ACFBC-23B2-EA45-9A12-BECFF07760FC.root + \
  --no_output + \
  --customise_commands "process.MessageLogger.files.out_$1 = dict(); process.Timing = cms.Service('Timing', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service('SimpleMemoryCheck', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"
else
  cmsDriver.py hgcal_tpg_validation -n 50 + \
  --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW + \
  --conditions auto:phase2_realistic_T15 + \
  --beamspot HLLHC14TeV + \
  --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation + \
  --geometry Extended2026D49 --era Phase2C9 + \
  --inputCommands "keep *","drop l1tTkPrimaryVertexs_L1TkPrimaryVertex__RECO" + \
  --filein file:/data_CMS_upgrade/data_jenkins/Phase2HLTTDRSummer20ReRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v2/003ACFBC-23B2-EA45-9A12-BECFF07760FC.root + \
  --no_output + \
  --customise_commands "process.MessageLogger.files.out_$1 = dict(); process.Timing = cms.Service('Timing', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service('SimpleMemoryCheck', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"
fi
