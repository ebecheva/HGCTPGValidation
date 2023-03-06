# Get the parameters for the particular subset
# python produceData_multiconfiguration.py --subsetconfig default_subset --label release
# release is ref or test

from schema import Schema, SchemaError
import yaml
import pprint
import os
import sys
import subprocess

sys.path.insert(0, '../../../HGCTPGValidation/scripts')
from configFunctions import check_schema_subset, check_schema_config, read_subset, read_config, get_listOfConfigs

# Run cmsDriver
def run_cmsDriver(configdata, release):
    configName=configdata['shortName']
    nbEvents=configdata['parameters']['nbOfEvents']
    conditions=configdata['parameters']['conditions']
    beamspot=configdata['parameters']['beamspot']
    geometry=configdata['parameters']['geometry']
    era=configdata['parameters']['era']
    inputCommands=configdata['parameters']['inputCommands']
    procModifiers=configdata['parameters']['procModifiers']
    filein=configdata['parameters']['filein']
    customiseUser=configdata['parameters']['customise']
    customiseUserCommand=configdata['parameters']['customise_commands']
    customiseCommand=f'{customiseUserCommand} "process.onlineSaver.tag = cms.untracked.string(\'validation_HGCAL_TPG_{configName}_{release}\'); process.MessageLogger.files.out_{configName}_{release} = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"'

    # If procModifiers==empty we get an empty string, so procModifiers is not used,
    # else --procModifiers {procModifiers} is added
    procMod = f'{"" if procModifiers=="empty" else f"--procModifiers {procModifiers}"}'
    
    # if customiseUser==empty we get an empty string, the --customise option won't be used
    # else --customise {customiseUser}
    customise = f'{"" if customiseUser=="empty" else f"--customise {customiseUser}"}'
    
    command = f"echo $PWD; source /cvmfs/cms.cern.ch/cmsset_default.sh; eval `scramv1 runtime -sh`; \
    cmsDriver.py hgcal_tpg_validation_{configName}_{release} -n {str(nbEvents)} \
    --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW \
    --conditions {conditions} \
    --beamspot {beamspot} \
    --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation \
    --geometry {geometry} --era {era} \
    --inputCommands {inputCommands} \
    {procMod} \
    --filein {filein} \
    --no_output \
    {customise} \
    --customise_commands {customiseCommand}"
    
    pprint.pprint(command)
    return command
    
def main(subsetconfig, release):
    logfile = open('logfile', 'w')
    logfile.write('Starts producing data from configurations.\n')
    
    # Path to the config files
    path='../../../HGCTPGValidation/config/'

    # read the subset_config file
    data = read_subset(path, subsetconfig)
    config = data["configuration"]
    for conf in config:
        # Read the configuration - key: value
        #- ref: default 
        #  test: bcstc
        for key, value in conf.items():
            # Do only for "test" or for "ref"
            if key==release:
              # Read the config file corresponding to key:value
              config_data=read_config(path, value)
              confName=config_data['shortName']
              # Generate and run the python configuration file with cmsDriver.py only if the file doesn't exist
              if os.path.exists(f"hgcal_tpg_validation_{confName}_{release}_USER.py"):
                print("Python file for the config ", value, ":", key, "was already created.")  
              else:
                command = run_cmsDriver(config_data, release)
                sourceCmd = ['bash', '-c', command]
                sourceProc = subprocess.Popen(sourceCmd, stdout=logfile, stderr=logfile)
                (out, err) = sourceProc.communicate() # wait for subprocess to finish
            else:
              print("Do not run this configuration: ", key, ": ", value)

if __name__ == "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--subsetconfig', dest='subsetconfig', help=' ', default='default_subset')
    parser.add_option('--label', dest='release', help=' ', default='test')
    (opt, args) = parser.parse_args()
   
    main(opt.subsetconfig, opt.release)
