# Get the parameters for the particular subset
# python ../../produceData_from_configuration.py --subsetconfig default_subset --label release
# release is ref or test

import yaml
import pprint
import os
import sys
import subprocess

# Read the subset file
def read_subset(config):
    print('config=',config)
    
    filename = config + '.yaml'
    print('filename = ', filename)
    
    with open('../../../HGCTPGValidation/config/' + filename) as f:
        subset = yaml.full_load(f)
     
        for item, config in subset.items():
            print(item, ":", config)
        
    return subset
    
# Read the configuration file
def read_config(config):
    
    filename = config + '.yaml'
    with open('../../../HGCTPGValidation/config/' + filename) as f:
        config = yaml.full_load(f)
        
        nbEvents=config['parameters']['nbOfEvents']
        os.system('python --version')
        
        for item, config in config.items():
            print(item, ":", config)
            
    return config

# Run cmsDriver
def run_cmsDriver(configdata, release):
    pprint.pprint(configdata['parameters']['nbOfEvents'])
    pprint.pprint(configdata['parameters']['conditions'])
    nbEvents=configdata['parameters']['nbOfEvents']
    conditions=configdata['parameters']['conditions']
    beamspot=configdata['parameters']['beamspot']
    geometry=configdata['parameters']['geometry']
    era=configdata['parameters']['era']
    inputCommands=configdata['parameters']['inputCommands']
    procModifiers=configdata['parameters']['procModifiers']
    filein=configdata['parameters']['filein']
    customise=configdata['parameters']['customise_commands']

    if procModifiers == 'empty':
        command = 'echo $PWD; source /cvmfs/cms.cern.ch/cmsset_default.sh; eval `scramv1 runtime -sh`; ' + \
        'cmsDriver.py hgcal_tpg_validation -n ' + str(nbEvents) + \
        ' --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW ' + \
        '--conditions ' + conditions + ' ' + \
        '--beamspot ' + beamspot + ' ' + \
        '--step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation ' + \
        '--geometry ' + geometry + ' ' + '--era ' + era + ' ' + \
        '--inputCommands ' + inputCommands + ' ' + \
        '--filein ' + filein + ' ' + \
        '--no_output ' + \
        '--customise_commands ' + customise + ' ' + '"process.MessageLogger.files.out_"' + release + '" = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"'
    else:
        command = 'echo $PWD; source /cvmfs/cms.cern.ch/cmsset_default.sh; eval `scramv1 runtime -sh`;' + \
        'cmsDriver.py hgcal_tpg_validation -n ' + str(nbEvents) + \
        ' --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW ' + \
        '--conditions ' + conditions + ' ' + \
        '--beamspot ' + beamspot + ' ' + \
        '--step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation ' + \
        '--geometry ' + geometry + ' ' + '--era ' + era + ' ' + '--inputCommands ' + inputCommands + ' ' + \
        '--procModifiers ' + procModifiers + ' ' + \
        '--inputCommands ' + inputCommands + ' ' + \
        '--filein ' + filein + ' ' + \
        '--no_output ' + \
        '--customise_commands ' + customise + ' ' + '"process.MessageLogger.files.out_"' + release + '"= dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"'
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
        print(type(config_data))
        nbEvents = config_data['parameters']['nbOfEvents']
        pprint.pprint(config_data['parameters']['nbOfEvents'])
        pprint.pprint(nbEvents)
        print("Print test config from main")
        for item, config_data in config_data.items():
            print(item, ":", config_data)
    
    pprint.pprint('Call cmsDriver')
    #command = run_cmsDriver(config_data, release)
    #---------- for test
    print(type(config_data))
    nbEvents=config_data['parameters']['nbOfEvents']
    conditions=config_data['parameters']['conditions']
    beamspot=config_data['parameters']['beamspot']
    geometry=config_data['parameters']['geometry']
    era=config_data['parameters']['era']
    inputCommands=config_data['parameters']['inputCommands']
    procModifiers=config_data['parameters']['procModifiers']
    filein=config_data['parameters']['filein']
    customise=config_data['parameters']['customise_commands']

    if procModifiers == 'empty':
        command = 'echo $PWD; source /cvmfs/cms.cern.ch/cmsset_default.sh; eval `scramv1 runtime -sh`; ' + \
        'cmsDriver.py hgcal_tpg_validation -n ' + str(nbEvents) + \
        ' --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW ' + \
        '--conditions ' + conditions + ' ' + \
        '--beamspot ' + beamspot + ' ' + \
        '--step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation ' + \
        '--geometry ' + geometry + ' ' + '--era ' + era + ' ' + \
        '--inputCommands ' + inputCommands + ' ' + \
        '--filein ' + filein + ' ' + \
        '--no_output ' + \
        '--customise_commands ' + customise + ' ' + '"process.MessageLogger.files.out_"' + release + '" = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"'
    else:
        command = 'echo $PWD; source /cvmfs/cms.cern.ch/cmsset_default.sh; eval `scramv1 runtime -sh`;' + \
        'cmsDriver.py hgcal_tpg_validation -n ' + str(nbEvents) + \
        ' --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW ' + \
        '--conditions ' + conditions + ' ' + \
        '--beamspot ' + beamspot + ' ' + \
        '--step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation ' + \
        '--geometry ' + geometry + ' ' + '--era ' + era + ' ' + '--inputCommands ' + inputCommands + ' ' + \
        '--procModifiers ' + procModifiers + ' ' + \
        '--inputCommands ' + inputCommands + ' ' + \
        '--filein ' + filein + ' ' + \
        '--no_output ' + \
        '--customise_commands ' + customise + ' ' + '"process.MessageLogger.files.out_"' + release + '"= dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"'
    pprint.pprint(command)
    #---------------------
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
