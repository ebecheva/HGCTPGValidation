#! /usr/bin/env python

import yaml
import pprint
import os
import sys
import subprocess

from schema import Schema, SchemaError

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
      print("Subset configuration is valid.")
    except SchemaErroras as se:
      print("The configuration format is not correct. Please check the file", filename)
      raise se
      
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
            "procModifiers": str,
            "filein": str,
            "customise": str,
            "customise_commands": str
        }
    })

    try:
        config_schema.validate(config)
    except SchemaError as se:
        print("The configuration format is not correct. Please check the file ", filename)
        raise se


# Read the file with configurations sets
def read_subset(path, config):
    filename = path + config + '.yaml'

    with open(filename) as f:
        try:
            subset = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print("Error occured when loading the file containing the configuration subsets file ", filename)
            print(e)

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
def read_config(path, configuration):
    filename = path + configuration + '.yaml'

    with open(filename) as f:
        try:
            config = yaml.safe_load(f)
            print("Read validation configuration file.")
        except yaml.YAMLError as e:
            print("Error occured when loading the configuration file ", filename)
            print(e)

    check_schema_config(config, filename)

    return config
