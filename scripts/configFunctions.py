#! /usr/bin/env python

import yaml
import pprint
import os
import sys
import subprocess

from schema import Schema, SchemaError, Optional

# Define the schema of the subset config file
def check_schema_subset(config, filename):
    config_schema = Schema({
        "subsetName": str,
        "description": str,
        "configuration": 
            [{"ref": str, "test": str}]
    })

    try:
      config_schema.validate(config)
    except SchemaError as se:
      print(f"\n\n === The configuration format is not correct. Please check the file {filename}. === \n\n {se}")
      raise Exception(f"\n\n === The configuration format is not correct. Please check the file {filename}. === \n\n {se}")
      
# Define the schema of the configuration data
def check_schema_config(config, filename):
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
            Optional("procModifiers", default=empty): str,
            "filein": str,
            Optional("customise", default=empty): str,
            Optional("customise_commands", default=''): str
        }
    })

    try:
        config_schema.validate(config)
    except SchemaError as se:
        print(f"\n\n === The configuration format is not correct. Please check the file {filename}. === \n\n {se}")
        raise Exception(f"\n\n The configuration format is not correct. Please check the file {filename}. === \n\n {se}")

# Define the schema of the config for the Jenkins job
# validating the validation code
def check_schema_paramValJob(config, filename):
    config_schema = Schema({
        "description": str,
        "parameters": {
            "cmsswRemote": str,
            "cmsswBranch": str
        }
    })

    try:
      config_schema.validate(config)
    except SchemaError as se:
      print(f"\n\n === The configuration format is not correct. Please check the file {filename}. === \n\n {se}")
      raise Exception(f"\n\n === The configuration format is not correct. Please check the file {filename}. === \n\n {se}")
 
# Read the file with configurations sets
def read_subset(path, config):
    filename = path + config + '.yaml'

    try:
        with open(filename) as f:
            subset = yaml.safe_load(f)
    except OSError as e:
        print(f"\n\n === Error occured when loading configuration subsets file {filename}. === \n\n {e}")
        raise Exception(f"\n\n === Error occured when loading configuration subsets file {filename}. === \n\n {e}")
    except yaml.YAMLError as e:
        print(f"\n\n === Error parsing YAML file: {filename} === \n\n {e}")
        raise Exception(f"\n\n === Error parsing YAML file: {filename}. === \n\n{e}")

    check_schema_subset(subset, filename)

    return subset


# Return a list with config pairs (ref, test)
def get_listOfConfigs(path, confSubsets):
    # read the subset_config file
    data = read_subset(path, confSubsets)
    config = data["configuration"]

    # List of configuration pairs (ref, test)
    subsets = []
    for conf in config:
        configValues = []
        # Read the configuration - key: value
        #- ref: default
        #  test: bcstc
        for release, confName in conf.items():
            configValues.append(confName)

        subsets.append(configValues)

    return subsets


# Read the configuration file
# config_type = 1 config files with the parameters for cmsDriver.py
# config_type = 2 config file with the parameters for the validation of the validation code 
def read_config(path, configuration, config_type):
    filename = path + configuration + '.yaml'

    try:
        with open(filename) as f:
            config = yaml.safe_load(f)
    except OSError as e:
        print(f"\n\n === Error occured when loading configuration file {filename}. === \n\n {e}")
        raise Exception(f"\n\n === Error occured when loading configuration file {filename} === \n\n {e}")
    except yaml.YAMLError as e:
        print(f"\n\n === Error parsing configuration YAML file: {filename}. === \n\n {e}")
        raise Exception(f"\n\n === Error parsing configuration YAML file: {filename}. === \n\n {e}")
    
    if (config_type == 1):
        check_schema_config(config, filename)
    elif (config_type == 2):
        check_schema_paramValJob(config, filename)
    else:
        print(f"\n\n === The config_type doesn't correspond to the defined validation types. === \n\n")

    return config
