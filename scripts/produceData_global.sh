#!/bin/bash

# ./produceData_global.sh subset_config_name $LABEL

echo "subset_config " $1
echo "label " $2

module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
module avail
module purge
module load python/3.9.9

python --version
python ../../../HGCTPGValidation/scripts/read_configuration_Jenkins.py --subsetconfig $1 --label $2

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
