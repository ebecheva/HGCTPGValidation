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
def run_cmsDriver(configdata, label, release_path):
    print("Run cmsDriver")
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
    #customiseCommand=f"{customiseUserCommand} process.onlineSaver.tag = cms.untracked.string(\'validation_HGCAL_TPG_{configName}_{label}\'); process.MessageLogger.files.out_{configName}_{label} = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"
    custCom=f"{customiseUserCommand}" + f"process.onlineSaver.tag = cms.untracked.string('validation_HGCAL_TPG_{configName}_{label}'); process.MessageLogger.files.out_{configName}_{label} = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"
    customiseCommand= '"' + custCom + '"'
    
    # If procModifiers==empty we get an empty string, so procModifiers is not used,
    # else --procModifiers {procModifiers} is added
    procMod = f'{"" if procModifiers=="empty" else f"--procModifiers {procModifiers}"}'
    
    # if customiseUser==empty we get an empty string, the --customise option won't be used
    # else --customise {customiseUser}
    customise = f'{"" if customiseUser=="empty" else f"--customise {customiseUser}"}'
    print("2 Current dir=", os.getcwd())
    
    command = ("echo $PWD; set -v; echo $$ $BASHPID ; ( echo $$ $BASHPID  ); " + "cd " + release_path + "; shopt -s expand_aliases; set +u && source /cvmfs/cms.cern.ch/cmsset_default.sh; set -u; " +
    "eval `scramv1 runtime -sh`; printenv; echo $PATH; ls -l ${CMS_PATH}/slc7_amd64_gcc10/cms/cmssw-patch/CMSSW_12_5_2_patch1/cfipython/slc7_amd64_gcc10/RecoHGCal/TICL")
    #"cmsDriver.py hgcal_tpg_validation_" + configName + "_" + label + " -n " + str(nbEvents) +
    #" --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW " +
    #"--conditions " + conditions +
    #" --beamspot " + beamspot +
    #" --step USER:'Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation'" +
    #" --geometry " + geometry + " --era " + era +
    #" --inputCommands " + inputCommands + " " + procMod +
    #" --filein " + filein +
    #" --no_output " + customise + " --customise_commands " + customiseCommand)
    
    print(command)
    return command
    
def main(subsetconfig, label, topdir, release):
    logfile = open('logfile', 'w')
    logfile.write('Starts producing data from configurations.\n')
    print('Starts producing data from configurations.\n')
    
    # Path to the config files
    config_path = f"{topdir}/HGCTPGValidation/config/"
    release_path = f"{topdir}/test_dir/{release}_HGCalTPGValidation_{label}/src/"
    
    # read the subset_config file
    data = read_subset(config_path, subsetconfig)
    config = data["configuration"]
    for conf in config:
        # Read the configuration - key: value
        #- ref: default 
        #  test: bcstc
        for key, value in conf.items():
            # Do only for "test" or for "ref"
            if key==label:
              print("config_path=", config_path)
              # Read the config file corresponding to key:value
              config_data=read_config(config_path, value)
              confName=config_data['shortName']
              print("config_data= ", config_data)
              # Generate and run the python configuration file with cmsDriver.py only if the file doesn't exist
              if os.path.exists(f"hgcal_tpg_validation_{confName}_{label}_USER.py"):
                print("Python file for the config ", value, ":", key, "was already created.")  
              else:
                cwd = os.getcwd()
                print("Current working directory:", cwd)
                command = run_cmsDriver(config_data, label, release_path)
                sourceCmd = ['/bin/bash', '-c', command]
                #sourceProc = subprocess.Popen(sourceCmd, stdout=logfile, stderr=logfile)
                #(out, err) = sourceProc.communicate() # wait for subprocess to finish
                sourceProc = subprocess.run(sourceCmd, stdout=logfile, stderr=logfile, check=True, text=True)
                #os.system(command)
            else:
              print("Do not run this configuration: ", key, ": ", value)

if __name__ == "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--subsetconfig', dest='subsetconfig', help=' ', default='default_subset')
    parser.add_option('--label', dest='label', help=' ', default='test')
    parser.add_option('--workspace', dest='topdir', help=' ', default='')
    parser.add_option('--release', dest='release', help=' ', default='')
    (opt, args) = parser.parse_args()
   
    main(opt.subsetconfig, opt.label, opt.topdir, opt.release)
