#!/bin/bash

# ./produceData.sh $LABEL

echo 'nbEvents= ' $nbEvents
echo 'conditions ' $conditions
echo 'beamspot ' $beamspot
echo 'geometry ' $geometry
echo 'era ' $era
echo 'procModifiers ' $procModifiers
echo 'filein ' $filein
echo 'customise ' $customise


source /cvmfs/cms.cern.ch/cmsset_default.sh
echo $PWD
eval `scramv1 runtime -sh`

if [[ $procModifiers != 'empty' ]]
then
cmsDriver.py hgcal_tpg_validation -n $nbEvents + \
  --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW + \
  --conditions $conditions + \
  --beamspot $beamspot + \
  --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation + \
  --geometry $geometry --era $era --procModifiers $procModifiers + \
  --inputCommands "keep *","drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT","drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT","drop l1tEMTFHit2016s_simEmtfDigis__HLT","drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT","drop l1tEMTFTrack2016s_simEmtfDigis__HLT" + \
  --filein $filein + \
  --no_output + \
  --customise_commands "$customise process.MessageLogger.files.out_$1 = dict(); process.Timing = cms.Service('Timing', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service('SimpleMemoryCheck', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"
else
cmsDriver.py hgcal_tpg_validation -n $nbEvents + \
  --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW + \
  --conditions $conditions + \
  --beamspot $beamspot + \
  --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation + \
  --geometry $geometry --era $era \
  --inputCommands "keep *","drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT","drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT","drop l1tEMTFHit2016s_simEmtfDigis__HLT","drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT","drop l1tEMTFTrack2016s_simEmtfDigis__HLT" + \
  --filein $filein + \
  --no_output + \
  --customise_commands "$customise process.MessageLogger.files.out_$1 = dict(); process.Timing = cms.Service('Timing', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service('SimpleMemoryCheck', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"
fi
