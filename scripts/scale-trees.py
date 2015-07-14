import sys
import os, commands
import shutil
from ROOT import *
import ROOT
from optparse import OptionParser

argv = sys.argv
parser = OptionParser()

parser.add_option("-d", "--useDAS", dest="useDAS", default=False, action="store_true",
                              help="Use # gen events from DAS")

(opts, args) = parser.parse_args(argv) 

inDirName = '/shome/thaarres/HiggsTagger/Spring15/rootfiles/qcd/'
outDirName = '/shome/thaarres/HiggsTagger/Spring15/rootfiles/qcd/scaled'
inTreeName = 'Fjets'
histName = "h_multiplicity"
targetFile = "qcd_forTrainingWeight1"
addcmd = "hadd -f %s/%s.root " %(outDirName,targetFile)
rmcmd = "rm "

n = 0 
for inFileName in os.listdir(inDirName):
  if inFileName.endswith(".root"):
    n += 1
    print "copying file %i" %n
    shutil.copy2("%s/%s" %(inDirName, inFileName), "%s/%s"%(outDirName, inFileName))
    inFile = TFile.Open( "%s/%s" %(outDirName, inFileName), "update" )
    if inFileName.find("300to470") != -1:
      xSec = 7823.0 #7475.
      genEv = 2930578 #events in DAS
    elif inFileName.find("470to600") != -1:
      xSec = 648.2# 587.1
      genEv = 1939229. #events in DAS
    elif inFileName.find("600to800") != -1:
      xSec = 186.9 #167.0
      genEv = 1890256. #events in DAS
    elif inFileName.find("800to1000") != -1:  
      xSec = 32.293 #28.25
      genEv = 1911296. #events in DAS
    elif inFileName.find("1000to1400") != -1:
      xSec = 9.4183 #8.195
      genEv = 1461216. #events in DAS
    elif inFileName.find("1400to1800") != -1:
      xSec = 0.842650 #0.7346
      genEv = 197959. #events in DAS
    else:
      print " Cross section not defined! Exiting..."
      sys.exit()
    if not opts.useDAS:
      genEv = inFile.Get(histName).GetEntries()
      print 'Not using gen events from DAS! Using %i events stored in %s' %(genEv,inFileName)
    weight = xSec/genEv
    
    myTree = inFile.Get( inTreeName )
    myTree.SetWeight(weight)
    myTree.AutoSave()

    addcmd+= ' %s/%s' %(outDirName, inFileName)
    rmcmd += ' %s/%s' %(outDirName, inFileName)

# os.system(addcmd)
print "Removing temporary files: ..."
# os.system(rmcmd)
inFile.Close()
del myTree