# Get the parameters for the particular subset
# displayHistos.py --subsetconfig subsetconfig_name --refdir refdir --testdir testdir 
# release is ref or test

#from schema import Schema, SchemaError
import yaml
import pprint
import os
import sys
import subprocess
from itertools import islice

#python2
import urllib
import re

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

topDirectory = os.getcwd()
print('topDirectory =', topDirectory)
sys.path.insert(0, './hgctpgvalidation/display')

from ROOT import TCanvas
from ROOT import TFile, gDirectory, TH1F
from graphFunctionsMulticonfigs_JobYaml import createWebPageLite, initRootStyle



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
def read_subset(config):
    print('config=',config)
    
    filename = config + '.yaml'
    print('filename = ', filename)
    
    with open('./config/' + filename) as f:
        try:
            subset = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
    
    return subset

# Return a list with config pairs (ref, test)  
def get_listOfConfigs(confSubsets):
    # read the subset_config file
    data = read_subset(confSubsets)
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

def checkSubprocessStatus(subProc, logfile):
    if subProc.wait() != 0:
       print('------------------------------------------------------------------------')
       print('=> Execution failed! There were some errors. Please, check the logfile.')
       print('------------------------------------------------------------------------')
       logfile.write('=> Execution failed! There were some errors.\n')
       sys.exit()
    else:
       print('Subprocess completed successfully!')
       logfile.write('=> Subprocess completed successfully!\n')

def extractInfos(namefile, dirname):
    # Output file MemoryReport_ref.log or MemoryReport_test.log
    indicator = namefile.split("_")
    #outputfile = f"MemoryReport_{indicator[1]}_{indicator[2]}"
    outputfile = "MemoryReport_" + indicator[1] + "_" + indicator[2]
    
    # Input file out_ref.log or out_test.log
    nfile = dirname + '/' + namefile
    # Number of lines to be read starting from the line " Time Summary:"
    number_of_lines = 18
    # Open the file to read
    with open(nfile) as f:
        # Open the file to fill with the extracted information
        with open(outputfile, "a+") as f1:
            for line in f:
                # Read Memory report information
                if "MemoryReport>" in line:
                    f1.writelines(line)
                # Read Time summary information
                if " Time Summary:" in line:
                    f1.writelines(line)
                    # Read 18 lines starting from " Time Summary:"
                    lines_cache = islice(f, number_of_lines)
                    for current_line in lines_cache:
                        f1.write(current_line)

def extract_time_info(refconfig, testconfig):
# Extract Time information for all modules
#find . -name "out_ref.log" | xargs grep "TimeModule>" > TimingInfo_ref.txt
#find . -name "out_test.log" | xargs grep "TimeModule>" > TimingInfo_test.txt
    print('extract_time_info starts')
    logfile = open('logfile', 'a+')
    logfile.write('extract_time_info starts\n')
    command = "find . -name \"out_" + refconfig + "_ref.log\" | xargs grep \"TimeModule>\" > TimingInfo_" + refconfig + "_ref.txt;  find . -name \"out_" + testconfig + "_test.log\" | xargs grep \"TimeModule>\" > TimingInfo_" + testconfig + "_test.txt"
    sourceCmd = ['bash', '-c', command]
    sourceProc = subprocess.Popen(sourceCmd, stdout=logfile, stderr=logfile)
    (out, err) = sourceProc.communicate() # wait for subprocess to finish
    checkSubprocessStatus(sourceProc, logfile)
    logfile.close()

#######################################################################################################################
# Read a file with the information from MemoryCheck and Time and fill corresponding histo (Nbr/Time/event)
# for each producer HGCalVFEProducer, HGCalConcentratorProducer, HGCalBackendLayer1Producer, HGCalBackendLayer2Producer,
# HGCalTowerMapProducer and HGCalTowerProducer
# rel is ref or test, configname is the name of the configuration
def readFileStatement(configname, rel, dirname):
    print('dirname = ', dirname)
    # Name of the file containing histograms
    rootFileName = "/DQM_V0001_validation_HGCAL_TPG_" + configname + "_" + rel + "_R000000001.root"
    rootFile = dirname + '/' + rootFileName
    print("rootFile = ", rootFile)
    
    # File to be read
    namefile = "TimingInfo_" + configname + "_" + rel + ".txt"
    
    # Open existing ROOT file
    hFile = TFile( rootFile, 'UPDATE' )
    # Places into the directory containing histograms
    topDir = gDirectory
    topDir.cd("DQMData/Run 1/HGCALTPG/Run summary")
    
    h_VFE = TH1F( 'h_VFE', 'HGCalVFEProducer: Time/event distribution', 1000, 0, 1.5 )
    h_Conc = TH1F( 'h_Conc', 'HGCalConcentratorProducer: Time/event distribution', 1000, 0, 0.5 )
    h_BackendL1 = TH1F( 'h_BackendL1', 'HGCalBackendLayer1Producer: Time/event distribution', 1000, 0, 1.5 )
    h_BackendL2 = TH1F( 'h_BackendL2', 'HGCalBackendLayer2Producer: Time/event distribution', 1000, 0, 0.5 )
    h_TowerMap = TH1F( 'h_TowerMap', 'HGCalTowerMapProducer: Time/event distribution', 1000, 0, 0.5 )
    h_Tower = TH1F( 'h_Tower', 'HGCalTowerProducer: Time/event distribution', 1000, 0, 0.5 )
    # list of histograms
    listHistos = [h_VFE, h_Conc, h_BackendL1, h_BackendL2, h_TowerMap, h_Tower]

    # list containing all name if producers
    listProducers=['HGCalVFEProducer', 'HGCalConcentratorProducer','HGCalBackendLayer1Producer','HGCalBackendLayer2Producer', 'HGCalTowerMapProducer','HGCalTowerProducer']
 
    # Open TimingInfo_.txt
    with open(namefile) as file:
        # Read data in the file
        data = file.readlines()
        for line in data:
            # Split a line and loop over it
            words=line.split()
            for i in range(len(listProducers)):
                if words[4]==listProducers[i]:
                    listHistos[i].Fill(float(words[5]))
                    # Set new histo range, -10% bellow the first non zero bin, and + 10% above the last non zero bin
                    if (listHistos[i].FindFirstBinAbove() != listHistos[i].FindLastBinAbove()):
                        add = int(listHistos[i].FindLastBinAbove()*0.10)
                        if (add == 0):
                            add = 5
                        listHistos[i].GetXaxis().SetRange(listHistos[i].FindFirstBinAbove() - add, listHistos[i].FindLastBinAbove() + add)
                    elif (listHistos[i].FindLastBinAbove() == 1):
                        listHistos[i].GetXaxis().SetRange(listHistos[i].FindFirstBinAbove(), listHistos[i].FindLastBinAbove() + 10)
    hFile.Write()

def standAloneHGCALTPGhistosCompare(refconfigname, testconfigname, refdir, testdir, imgdir):
    # graphical initialization
    initRootStyle()
    cnv = TCanvas("canvas")
    
    os.system("mkdir " + imgdir)
    os.system("mkdir " + imgdir + "/img")
    
    # Files names
    filename_ref = "/DQM_V0001_validation_HGCAL_TPG_" + refconfigname + "_ref_R000000001.root"
    filename_test = "/DQM_V0001_validation_HGCAL_TPG_" + testconfigname + "_test_R000000001.root"
    input_ref_file = refdir + filename_ref
    input_test_file = testdir + filename_test
    path_1 = 'DQMData/Run 1/HGCALTPG/Run summary'
    path_2 = path_1
    print('input_ref_file=', input_ref_file)
    print('input_test_file=', input_test_file)
    
    # web page creation. Title and others items are included into the createWebPage() function.
    createWebPageLite(refconfigname, testconfigname, input_ref_file, input_test_file, path_1, path_2, cnv, imgdir)

    print("Fin.")

def writeIntoFile(prnumber, configTest, configRef, prtitle, prdir):
    fileName = prdir + "/validation_webpages.txt"
    with open(fileName, 'a') as f:
        prnb  = "PR" + prnumber
        if config=='':
            title = prnb + " : " + prtitle + "\n"
        else:
            title = "Test: " + configTest + " | " + "Ref: " + configRef + "\n"
        f.write(title) 

def main(configset, refdir, testdir, datadir, prnumber, prtitle):
    print('configset=', configset)
    logfile = open('logfile', 'w')
    logfile.write('Subprocess starts\n')
    logfile.write(prnumber)
    
    prdir = "../../" + datadir + "/PR" + prnumber
    
    # Create directory with compared histogrames
    if os.path.exists(prdir):
        print("The data directory for the PR ", prdir, "already exists.")
        mess = "The data directory for the PR " + prdir + "already exists."
        logfile.write(mess)
        os.system("rm -rf " + prdir)
    else:
        print("The data directory for the PR ", prdir, "doesn't exist.")
        mess = "The data directory for the PR " + prdir + "doesn't exist."
        logfile.write(mess)
    
    os.system("mkdir " + prdir)
    
    # Write the first line of the validation_webpages.txt
    writeIntoFile(prnumber,'', '', prtitle, prdir)
    
    configSubsets = get_listOfConfigs(configset)
    # Loop over all pairs of configs (ref-test)
    for elem in configSubsets:
        print(elem[1] + " - " + elem[0])
        conf = elem[1] + "_" + elem[0]
        confRef = elem[0]
        confTest = elem[1]
        # Extract Time information for all modules
        extract_time_info(elem[0], elem[1])
     
        # Extract Memory Check information and global Time information   
        extractInfos("out_" + confRef + "_ref.log", refdir)
        extractInfos("out_" + confTest + "_test.log", testdir)
     
        # Create histograms Time/event/producer from TimingInfo_.txt 
        readFileStatement(confRef, "ref", refdir)
        readFileStatement(confTest, "test", testdir)
        
        # For each pair (release-config) compare histograms and create web pages
        # The directory containing the images is labeled with the ref and test config names
        # The name wille be GIF_confTest_confRef
        imgdir = "GIF_" + conf
        standAloneHGCALTPGhistosCompare(confRef, confTest, refdir, testdir, imgdir)
        
        # Create directories for data, 
        # prnumber: directory for a particular PR
        # prnumberconfig: one directory per config for a given PR
        prnumberconfig = "PR" + prnumber + "_" + conf
        datadir_gif = datadir + "/PR" + prnumber + "/" + prnumberconfig
        print("datadir=", datadir)
        print("prnumberconfig=", prnumberconfig)
        print("datadir_gif=", datadir_gif)
        
        if os.path.exists(datadir_gif):
            print("The data directory ", datadir_gif, "already exists.")
            mess1="The data directory " + datadir_gif + "already exists."
            logfile.write(mess1)
        else:
            os.system("mkdir " + datadir_gif)
            print("cp -rf " + imgdir + " /." + datadir_gif)
            os.system("cp -rf " + imgdir + " /. " + datadir_gif)
            writeIntoFile(prnumber, confTest, confRef, prtitle, prdir)
     
if __name__=='__main__':
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--subsetconfig', dest='subsetconfig', help=' ', default='default')
    parser.add_option('--refdir', dest='refdir', help=' ', default='')
    parser.add_option('--testdir', dest='testdir', help=' ', default='')
    parser.add_option('--datadir', dest='datadir', help=' ', default='')
    parser.add_option('--prnumber', dest='prnumber', help=' ', default='')
    parser.add_option('--prtitle', dest='prtitle', help=' ', default='', type="string")
    (opt, args) = parser.parse_args()

    main(opt.subsetconfig, opt.refdir, opt.testdir, opt.datadir, opt.prnumber, opt.prtitle)
