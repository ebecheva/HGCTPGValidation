#! /usr/bin/env python

import yaml
import pprint
import os
import sys
import subprocess

from schema import Schema, SchemaError

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


# Read the file with configurations sets
def read_subset(path, config):
    print('path=', path)
    print('config=', config)

    filename = path + config + '.yaml'
    print('filename = ', filename)

    with open(filename) as f:
        try:
            subset = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)

    return subset


# Return a list with config pairs (ref, test)
def get_listOfConfigs(path, confSubsets):
    # read the subset_config file
    data = read_subset(path, confSubsets)
    config = data["configuration"]

    # List of configuration pairs (ref, test)
    subsets = []
    for conf in config:
        print(conf)
        configValues = []
        # Read the configuration - key: value
        #- ref: default
        #  test: bcstc
        for release, confName in conf.items():
            configValues.append(confName)
            print("key = ", release, "value = ", confName)

        subsets.append(configValues)

    return subsets


# Read the configuration file
def read_config(path, configuration):
    os.system('python --version')
    filename = path + configuration + '.yaml'

    with open(filename) as f:
        try:
            config = yaml.safe_load(f)
            print("Read simulation configuration file.")
            print(config)
        except yaml.YAMLError as e:
            print(e)

    check_schema_config(config)

    return config
