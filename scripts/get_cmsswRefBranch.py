# Get the parameters for the job validating the validation code
# get_cmsswRefBranch.py

from schema import Schema, SchemaError
import yaml
import pprint
import os
import sys
import subprocess

sys.path.insert(0, './HGCTPGValidation/scripts')
from configFunctions import check_schema_paramValJob, read_config


def main():
    logfile = open('logfile', 'w')
    logfile.write('Starts producing data from configurations.\n')
    
    # Configuration name used for the validation of the validation code
    configuration = 'job_val_params'
    
    # Path to the config files
    path='./HGCTPGValidation/config/'
    
    # read the configuration file
    data = read_config(path, configuration, 2)
    baseBranch=data['parameters']['cmsswBranch']
    print(baseBranch)

if __name__ == "__main__":
    main()
