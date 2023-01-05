# Get the parameters for the particular subset
# python produceData_multiconfiguration.py --subsetconfig default_subset --label release
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
    configName=configdata['shortName']
    nbEvents=configdata['parameters']['nbOfEvents']
    conditions=configdata['parameters']['conditions']
    beamspot=configdata['parameters']['beamspot']
    geometry=configdata['parameters']['geometry']
    era=configdata['parameters']['era']
    inputCommands=configdata['parameters']['inputCommands']
    procModifiers=configdata['parameters']['procModifiers']
    filein=configdata['parameters']['filein']
    customiseUser=configdata['parameters']['customise_commands']
    customise=f'{customiseUser} "process.onlineSaver.tag = cms.untracked.string(\'validation_HGCAL_TPG_{configName}_{release}\'); process.MessageLogger.files.out_{configName}_{release} = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"'
 
    if procModifiers == 'empty':
        command = f"echo $PWD; source /cvmfs/cms.cern.ch/cmsset_default.sh; eval `scramv1 runtime -sh`; \
        cmsDriver.py hgcal_tpg_validation_{configName}_{release} -n {str(nbEvents)} \
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
        cmsDriver.py hgcal_tpg_validation_{configName}_{release} -n {str(nbEvents)} \
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
    print('subsetconfig=',subsetconfig)
    logfile = open('logfile', 'w')
    logfile.write('Subprocess starts\n')
    
    # read the subset_config file
    data = read_subset(subsetconfig)
    config = data["configuration"]
    #print(config)
    print(os.getcwd()) 
    for conf in config:
        #print(conf)
        # Read the configuration - key: value
        #- ref: default 
        #  test: bcstc
        for key, value in conf.items():
            print("key = ", key, "value = ", value)
            # Do only for "test" or for "ref"
            if key==release:
              # Read the config file corresponding to key:value
              config_data=read_config(value)
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
