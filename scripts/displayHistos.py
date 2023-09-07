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
sys.path.insert(0, '../HGCTPGValidation/hgctpgvalidation/display')

from ROOT import TCanvas
from ROOT import TFile, gDirectory, TH1F
from graphFunctionsMulticonfigs import createWebPageLite, initRootStyle
from configFunctions import get_listOfConfigs, check_schema_config, read_config 

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

# Extract Memory Check information and global Time information
def	extractTimeMemoryInfos(namefile, dirname):
    print("Extract Time&Memory information from ", namefile)
        
    # Output file MemoryReport_ref.log or MemoryReport_test.log
    indicator = namefile.split("_")
    #outputfile = f"MemoryReport_{indicator[1]}_{indicator[2]}"
    outputfile = "MemoryReport_" + indicator[1] + "_" + indicator[2]
    print("oututfile = ", outputfile)
    
    # Input file out_ref.log or out_test.log
    nfile = dirname + '/' + namefile
    
    if os.path.exists(nfile):
    # Remove Memory.txt files
        print("The file ", outputfile, "already exists. It will be deleted.")
        os.system("rm " + outputfile)
    else:
        print("The file ", outputfile, "wille be created.")
        
    # Open the file to read
    with open(nfile) as f:
    # Open the file to fill with the extracted information
        with open(outputfile, "w") as f1:
            for line in f:
                # Read Memory report information
                # Extract the value of the peak
                if "MemoryReport>" in line:
                    indicator = line.split(" ")
                    print(f"{indicator[4]} {indicator[5]}")
                    f1.writelines(f"{indicator[4]} {indicator[5]}")
                    # Read Time summary information
                if " Time Summary:" in line:
                    #f1.writelines(line)
                    # Read 18 lines starting from " Time Summary:"
                    lines_cache = islice(f, 2, 5, None)
                    for current_line in lines_cache:
                        indicator = current_line.split(" ")
                        if (indicator[2])=="Avg":
                            print(indicator[6])
                            f1.write(indicator[6])
                        else:
                            print(indicator[5])
                            f1.write(indicator[5])

# Extract Time information for all modules
#find . -name "out_ref.log" | xargs grep "TimeModule>" > TimingInfo_ref.txt
#find . -name "out_test.log" | xargs grep "TimeModule>" > TimingInfo_test.txt
def extract_time_info(refconfig, testconfig):
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
    print("Call standAloneHGCALTPGhistosCompare.")
    # graphical initialization
    initRootStyle()
    cnv = TCanvas("canvas")
    
    if os.path.exists(imgdir):
      print("The path " + imgdir + "exists. Will be deleted.")
      os.system("rm -rf " + imgdir)
      
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
    print("Call writeIntoFile.")
    
    fileName = prdir + "/validation_webpages.txt"
    print(fileName)
    with open(fileName, 'a') as f:
        prnb  = "PR" + prnumber
        if configTest=='':
            title = prnb + " : " + prtitle + "\n"
        else:
            title = prnb + "_" + configTest + "_" + configRef + " : Test: " + configTest + " | " + "Ref: " + configRef + "\n"
        f.write(title)

def main(configset, refdir, testdir, datadir, prnumber, prtitle):
    print(' == Main == ')
    print('configset=', configset)
    print('refdir=', refdir)
    print('testdir=', testdir)
    print('datadir=', datadir)
    print('prnumber=', prnumber)
    print('prtitle=', prtitle)
    logfile = open('logfile', 'w')
    logfile.write('Subprocess starts\n')
    logfile.write(prnumber)
    
    # Create directory with compared histogrames
    prdir = "../../" + datadir + "/PR" + prnumber
    print('prdir = ', prdir)
    if os.path.exists(prdir):
        # Remove directory before copying new histograms, this is used when running only Display script
        # When running the job with Jenkins, this directory is removed at the beginning of the job
        print("The data directory for the PR ", prdir, "already exists. It will be deleted.")
        mess = "The data directory for the PR " + prdir + "already exists. It will be deleted."
        logfile.write(mess)
        #os.system("ls -lrt " + prdir)
        os.system("rm -rf " + prdir)
    else:
        print("The data directory for the PR ", prdir, "doesn't exist. It will be created")
        mess = "The data directory for the PR " + prdir + "doesn't exist. It will be created"
        logfile.write(mess)
    
    print("Will do mkdir " + prdir)
    os.system("mkdir " + prdir)
    os.system("ls -lrt " + prdir)

    # Write the first line of the validation_webpages.txt
    writeIntoFile(prnumber, '', '', prtitle, prdir)
    
    # Path to the config file
    path='../HGCTPGValidation/config/'
    configSubsets = get_listOfConfigs(path, configset)
    # Loop over all pairs of configs (ref-test)
    for elem in configSubsets:
        print(elem[1] + " - " + elem[0])
        conf = elem[1] + "_" + elem[0]
        confRef = elem[0]
        confTest = elem[1]
        
        # If the validation is performed only for test release, this release is compared to itself
        # Create the missing files for the ref configuration
        if testdir==refdir:
            print("testdir and refdir are the same.")
            print("cp out_" + confTest + "_test.log out_" + confRef + "_ref.log")
            currDir = os.getcwd()
            print('currDir = ', currDir)
            # Copy out_config_test.log to out_config_ref.log
            os.system("cp " + testdir + "/out_" + confTest + "_test.log " + testdir + "/out_" + confRef + "_ref.log")
            # Copy DQM...config_test.root to DQM...config_ref.root
            os.system("cp " + testdir + "/DQM_V0001_validation_HGCAL_TPG_" + confTest + "_test_R000000001.root " + testdir + "/DQM_V0001_validation_HGCAL_TPG_" + confRef + "_ref_R000000001.root") 
            os.system("ls -lrt")
        else:
            print("testdir and refdir are different.")
        
        # Extract Time information for all modules
        extract_time_info(confRef, confTest)
        
        # Extract Memory Check information and global Time information
        extractTimeMemoryInfos("out_" + confTest + "_test.log", testdir)
        extractTimeMemoryInfos("out_" + confRef + "_ref.log", refdir)
     
        # Create histograms Time/event/producer from TimingInfo_.txt 
        readFileStatement(confRef, "ref", refdir)
        readFileStatement(confTest, "test", testdir)
        
        # For each pair (release-config) compare histograms and create web pages
        # The directory containing the images is labeled with the ref and test config names
        # The name wille be GIF_confTest_confRef
        imgdir = "GIF_" + conf
        standAloneHGCALTPGhistosCompare(confRef, confTest, refdir, testdir, imgdir)
        
        # Create data directories for each configuration, 
        # prnumber: directory for a particular PR
        # prnumberconfig: one directory per config for a given PR
        prnumberconfig = "PR" + prnumber + "_" + conf
        datadir_gif = prdir + "/" + prnumberconfig
        print("datadir = ", datadir)
        print("prnumberconfig = ", prnumberconfig)
        print("datadir_gif = ", datadir_gif)
        currentDirectory = os.getcwd()
        print('currentDirectory = ', currentDirectory)

        if os.path.exists(datadir_gif):
            print("The data directory ", datadir_gif, "already exists.")
            mess1="The data directory " + datadir_gif + "already exists."
            logfile.write(mess1)
        else:
            print("Directory " + datadir_gif + " will be created.")
            os.system("mkdir " + datadir_gif)
            print("cp -rf " + imgdir + "/. " + datadir_gif)
            os.system("cp -rf " + imgdir + "/. " + datadir_gif)
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
