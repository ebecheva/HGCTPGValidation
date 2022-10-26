
# Get the parameters for the particular subset
# python produceData_from_configuration.py --subsetconfig default_subset --label release
# release is ref or test

from schema import Schema, SchemaError
import yaml
import pprint
import os
import sys
import subprocess

# Define the schema of the subset config file
def check_schema_subset(config):
    config_schema = Schema({
        "subsetName": str,
        "description": str,
        "configuration": {
            "ref": str,
            "test": str
        }
    })

    try:
      config_schema.validate(config)
      print("Subset configuration is valid.")
    except SchemaErroras as se:
      raise se

# Define the schema of the configuration data
def check_schema_config(config):
    config_schema = Schema({
        "shortName": str,
        "longName": str,
        "description": str,
        "parameters": {
            "nbOfEvents": int,
            "conditions": str,
            "beamspot": str,
            "geometry": str,
            "era": str,
            "inputCommands": str,
            "procModifiers": str,
            "filein": str,
            "customise_commands": str
        }
    })

    try:
        config_schema.validate(config)
        print("Configuration is valid.")
    except SchemaError as se:
        raise se
    
# Read the subset file
def read_subset(config):
    print('config=',config)
    
    filename = config + '.yaml'
    print('filename = ', filename)
    
    with open('../../../HGCTPGValidation/config/' + filename) as f:
        try:
            subset = yaml.safe_load(f)
            print("Read subset configuration file.")
            print(subset)
        except yaml.YAMLError as e:
            print(e)
    
    return subset
    
# Read the configuration file
def read_config(configuration):
    os.system('python --version')
    filename = configuration + '.yaml'
    with open('../../../HGCTPGValidation/config/' + filename) as f:
        try:
            config = yaml.safe_load(f)
            print("Read simulation configuration file.")
            print(config)          
        except yaml.YAMLError as e:
            print(e)
    
    check_schema_config(config)
    
    return config

# Run cmsDriver
def run_cmsDriver(configdata, release):
    pprint.pprint('Running cmsDriver')
    nbEvents=configdata['parameters']['nbOfEvents']
    conditions=configdata['parameters']['conditions']
    beamspot=configdata['parameters']['beamspot']
    geometry=configdata['parameters']['geometry']
    era=configdata['parameters']['era']
    inputCommands=configdata['parameters']['inputCommands']
    procModifiers=configdata['parameters']['procModifiers']
    filein=configdata['parameters']['filein']
    customiseUser=configdata['parameters']['customise_commands']
    customise=f'{customiseUser} "process.MessageLogger.files.out_{release} = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"'

    if procModifiers == 'empty':
        command = f"echo $PWD; source /cvmfs/cms.cern.ch/cmsset_default.sh; eval `scramv1 runtime -sh`; \
        cmsDriver.py hgcal_tpg_validation -n {str(nbEvents)} \
         --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW \
        --conditions {conditions} \
        --beamspot {beamspot} \
        --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation \
        --geometry {geometry} --era {era} \
        --inputCommands {inputCommands} \
        --filein {filein} \
        --no_output \
        --customise_commands {customise}"    
    else:
        command = f"echo $PWD; source /cvmfs/cms.cern.ch/cmsset_default.sh; eval `scramv1 runtime -sh`; \
        cmsDriver.py hgcal_tpg_validation -n {str(nbEvents)} \
         --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW \
        --conditions {conditions} \
        --beamspot {beamspot} \
        --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation \
        --geometry {geometry} --era {era} \
        --inputCommands {inputCommands} \
        --procModifiers {procModifiers} \
        --filein {filein} \
        --no_output \
        --customise_commands {customise}"
    
    pprint.pprint(command)
    return command
    
def main(subsetconfig, release):

    # read the subset_config file
    data = read_subset(subsetconfig)
    refer=data['configuration']['ref']
    test=data['configuration']['test']
    print("ref config: ",refer)
    print("test config: ",test)
    
    logfile = open('logfile', 'w')
    logfile.write('Subprocess starts\n')
    
    # read the configuration file
    if release=="ref":
        print("Read config for ref release")  
        config_data=read_config(refer)
    elif release=="test":
        print("Read config for test release")
        config_data = read_config(test)
    else:
        print("The configuration doesn't contain the right name of release.")
    
    # The configuration data will be used to generate a python script by cmsDriver 
    # and run the simulation+validation 
    command = run_cmsDriver(config_data, release)

    sourceCmd = ['bash', '-c', command]
    sourceProc = subprocess.Popen(sourceCmd, stdout=logfile, stderr=logfile)
    (out, err) = sourceProc.communicate() # wait for subprocess to finish

if __name__ == "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--subsetconfig', dest='subsetconfig', help=' ', default='default_subset')
    parser.add_option('--label', dest='release', help=' ', default='test')
    (opt, args) = parser.parse_args()
   
    main(opt.subsetconfig, opt.release)
    
