# Get the parameters for the particular subset
# read_configuration_Jenkins.py --subsetconfig subsetconfig_name --label release
# release is ref or test

import yaml
import pprint
import os
import sys


def read_subset(config):
    print('config=',config)
    
    filename = config + '.yaml'
    print('filename = ', filename)
       
    with open('../../../HGCTPGValidation/config/' + filename) as f:
        subset = yaml.full_load(f)
     
        for item, config in subset.items():
            print(item, ":", config)
        
    return subset
    

def read_config(config):
    
    filename = config + '.yaml'
    with open('../../../HGCTPGValidation/config/' + filename) as f:
        config = yaml.full_load(f)
        
        #for item, config in config.items():
        #    print(item, ":", config)
            
    return config

def main(subsetconfig, release):

    # read the subset_config file
    data = read_subset(subsetconfig)
    refer=data['configuration']['ref']
    test=data['configuration']['test']
    print("ref config: ",refer)
    print("test config: ",test)
    
    # read the configuration file
    if release=="ref":
        print("Read config for ref release")  
        config_data=read_config(refer)
    elif release=="test":
        print("Read config for test release")
        config_data=read_config(test)
    
    pprint.pprint(config_data['parameters']['nbOfEvents'])
    pprint.pprint(config_data['parameters']['conditions'])
    os.putenv("nbEvents",str(config_data['parameters']['nbOfEvents']))
    os.putenv("conditions",str(config_data['parameters']['conditions']))
    os.putenv("beamspot",str(config_data['parameters']['beamspot']))
    os.putenv("geometry",str(config_data['parameters']['geometry']))
    os.putenv("era",str(config_data['parameters']['era']))
    os.putenv("procModifiers",str(config_data['parameters']['procModifiers']))
    os.putenv("filein",str(config_data['parameters']['filein']))
    os.putenv("customise",str(config_data['parameters']['customise_commands']))
    os.system('sh')

if __name__ == "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--subsetconfig', dest='subsetconfig', help=' ', default='subset1')
    parser.add_option('--label', dest='release', help=' ', default='test')
    (opt, args) = parser.parse_args()
   
    main(opt.subsetconfig, opt.release)
