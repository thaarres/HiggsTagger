from optparse import OptionParser
import sys
import ConfigParser
from ROOT import *
import os
import multiprocessing
import array
 
training_vars_float = [
  "z_ratio",#*(SV_vtx_pt_0+SV_vtx_pt_1)/(SV_mass_0+SV_mass_1)",
  "tau_dot",
  "SV_mass_0",
#  "z_ratio1",
#  "z_ratio2",
  "SV_vtx_EnergyRatio_0",
  "SV_vtx_EnergyRatio_1",
#  "SV_vtx_deltaR_0", 
  "PFLepton_ratio",
  "PFLepton_ptrel",
  # "massPruned",
#  "tau2/tau1",
#   "SV_flight2D_0",
#   "SV_flight2D_1",
#   "SV_flight2DErr_0",
#   "SV_flight2DErr_1",
#   "SV_totCharge_0",
#   "SV_totCharge_1",
  #"SV_mass_1",
#  "SV_vtx_pt_0",
#  "SV_vtx_pt_1",
#  "SV_vtx_deltaR_1",
  "trackSip3dSig_3"
#  "trackPtRel_0",
#  "trackSip3dSig_2",
  #"trackSip3dSig_1",
  #"trackPtRel_1",
  #"trackSip3dSig_0",
  #"trackPtRel_0",
  #"trackPtRel_2",
  #"trackEtaRel_0",
  #"trackEtaRel_1",
  #"trackEtaRel_2",
  #"PFLepton_ratioRel",
  #"PFLepton_deltaR",
  ]
 
training_vars_int = [
  # "nSV",
   #"nSL_3", 		
   "nSL_3",
  # "SV_nTrk_0",
  # "SV_nTrk_1",
   "jetNTracksEtaRel" 
  ]

argv = sys.argv
parser = OptionParser()
parser.add_option("-c", "--categories", dest="categories", default=False, action="store_true",
                              help="train in pt-eta categories")
parser.add_option("-w", "--weight", dest="weight", default=False, action="store_true",
                              help="pt-eta reweight")
parser.add_option("-g", "--gluonsplitting", dest="gluonsplitting", default=False, action="store_true",
                              help="train bb vs. gsp")
parser.add_option("-C", "--charm", dest="charm", default=False, action="store_true",
                              help="train bb vs. charm") 
parser.add_option("-p", "--usePT", dest="usePT", default=False, action="store_true",
                              help="use pT in training")                      
parser.add_option("-f", "--file", dest="filename",
                  help="write to FILE", metavar="FILE")                                                                                                                                                                               			      			      			      			      
(opts, args) = parser.parse_args(argv)  

def train(bdtoptions):

  outFile = TFile('TMVA_baseline.root', 'RECREATE')
  print "Printing output to %s" %outFile.GetName()

  factory = TMVA.Factory(
                               "TMVAClassification", 
                               outFile, 
                               # "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification"
                               "!V:!Silent:Color:DrawProgressBar:Transformations=I:AnalysisType=Classification"
                             )
  
  TMVA_tools = TMVA.Tools.Instance()
  treeS = TChain('Fjets')
  treeB = TChain('Fjets')
  treelist = []
  
  # prefix = 'Spring15/rootfiles/qcd/scaled/'
 #  files = [
 #      'qcd_1000to1400_spring15_forTraining.root',
 #      'qcd_1400to1800_spring15_forTraining.root',
 #      'qcd_300to470_spring15_forTraining.root',
 #      'qcd_470to600_spring15_forTraining.root',
 #      'qcd_600to800_spring15_forTraining.root',
 #      'qcd_800to1000_spring15_forTraining.root'
 #    ]
 #
 #  for f in files:
 #    print 'Opening file %s' %f
 #    filetmp = prefix + f
 #    file = TFile.Open(filetmp, 'READ')
 #    tree = file.Get("Fjets")
 #    weight = tree.GetWeight()
 #    print "weight = %f" %weight
 #    factory.AddBackgroundTree(tree, weight)
 #    treeB.Add(filetmp)
 #    print 'Setting weight to %f' %weight

  treeB.Add('Spring15/qcd_forTraining.root')
  treeS.Add('Spring15/rAll_forTraining.root')
  factory.AddSignalTree(treeS, 1.)
  factory.AddBackgroundTree(treeB, 1.)
  
  signal_selection = '' # bb massPruned>80 && massPruned<150
  print "Signal selection = %s" %signal_selection
  
  if(opts.gluonsplitting):
    background_selection = 'abs(flavour==5) && nbHadrons>1' #gsp massPruned>80 && massPruned<150 &&
  elif(opts.charm):
    background_selection = 'abs(flavour==4)' # charm
  else:
    background_selection = '' # no b
  
  print "Bkg selection = %s" %background_selection
  num_pass = treeS.GetEntries(signal_selection)
  num_fail = treeB.GetEntries(background_selection)

  print 'N events signal', num_pass
  print 'N events background', num_fail
  

  for var in training_vars_float:
    print "Adding variable: %s" %var
    factory.AddVariable(var, 'F') # add float variable
  for var in training_vars_int:
    factory.AddVariable(var, 'I') # add integer variable
  
  if(opts.usePT):  
    factory.AddVariable("ptPruned", 'F')
  
  
  factory.AddSpectator("massPruned")
  factory.AddSpectator("flavour")
  factory.AddSpectator("nbHadrons")  

  if not opts.usePT: 
     factory.AddSpectator("ptPruned")
  
  factory.AddSpectator("etaPruned")
  factory.AddSpectator("SubJet_csv")
    
  if (opts.weight):
    # factory.AddSpectator("weight_etaPt")
    factory.SetWeightExpression('weight_etaPt')
  # else:
    # factory.SetWeightExpression('1.')
    
  
  factory.PrepareTrainingAndTestTree( TCut(signal_selection), TCut(background_selection), 
      # "nTrain_Signal=0::nTest_Signal=0:nTrain_Background=20000:nTest_Background=20000:SplitMode=Random:!V" )
      "nTrain_Signal=0::nTest_Signal=0:nTrain_Background=20000:nTest_Background=20000:SplitMode=Random:!V" )
      # "nTrain_Signal=30000:nTest_Signal=12000:nTrain_Background=30000:nTest_Background=50000:SplitMode=Random:!V" )
      
  # factory.BookMethod( TMVA.Types.kFisher, "Fisher", "!H:!V:Fisher" )
  factory.BookMethod( TMVA.Types.kBDT,
                      "BDTG",
                      "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedGrad:GradBaggingFraction=0.9:SeparationType=GiniIndex:nCuts=500:NNodesMax=5"
                      #":".join(bdtoptions)
                    )
  
  if (opts.categories):
    
    if(opts.usePT):  
      theCat1Vars = "PFLepton_ptrel:z_ratio1:tau_dot:SV_mass_0:SV_vtx_EnergyRatio_0:SV_vtx_EnergyRatio_1:PFLepton_IP2D:tau2/tau1:nSV:nSL:ptPruned"
    else:
      theCat1Vars = "PFLepton_ptrel:z_ratio1:tau_dot:SV_mass_0:SV_vtx_EnergyRatio_0:SV_vtx_EnergyRatio_1:PFLepton_IP2D:tau2/tau1:nSV:nSL"
    
    mcat2 = factory.BookMethod( TMVA.Types.kCategory, "BDTCat8","" )  
    cuts2 = [
      'abs(etaPruned)<=1.4 && ptPruned <450', 'abs(etaPruned)<=1.4 && ptPruned >= 450 && ptPruned < 600', 'abs(etaPruned)<=1.4 && ptPruned >= 600 && ptPruned < 800', 'abs(etaPruned)<=1.4 && ptPruned >= 800',
      'abs(etaPruned)>1.4 && ptPruned <450', 'abs(etaPruned)>1.4 && ptPruned >= 450 && ptPruned < 600', 'abs(etaPruned)>1.4 && ptPruned >= 600 && ptPruned < 800', 'abs(etaPruned)>1.4 && ptPruned >= 800'
    ]
 
    for cut in cuts2:
      print "Training in category %s" %cut
      mcat2.AddMethod( TCut(cut), theCat1Vars, TMVA.Types.kBDT, "Category_BDT_8","!H:!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=4" )
  
  
  # (TMVA.gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 2
  factory.TrainAllMethods()
  # factory.OptimizeAllMethods()

  factory.TestAllMethods()

  # factory.EvaluateAllMethods()

  outFile.Close()

  # gLoadMacro('$ROOTSYS/tmva/test/TMVAGui.C')
  # TMVAGui('TMVA_classification.root')
  # raw_input("Press Enter to continue...")

# # def read(inDirName, inFileName):
def read(inDirName, inFileName):
  print "Reading", inFileName
  print "################################"

  TMVA_tools = TMVA.Tools.Instance()

  tree = TChain('Fjets')
  tree.Add('%s%s' %(inDirName,inFileName))
  print '%s%s' %(inDirName,inFileName)
  print "################################"
  print "################################"
  print "################################"
  reader = TMVA.Reader('TMVAClassification_BDTG')
  
  etaPruned = array.array('f',[0])
  ptPruned = array.array('f',[0])
  flavour = array.array('f',[0])
  nbHadrons = array.array('f',[0])
  massPruned = array.array('f',[0])
  SubJet_csv = array.array('f',[0])

  
  varDict = {}
  for var in training_vars_float:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])
  for var in training_vars_int:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])
    
  if(opts.usePT):
    reader.AddVariable("ptPruned",ptPruned)

  reader.AddSpectator("massPruned", massPruned)
  reader.AddSpectator("flavour", flavour)
  reader.AddSpectator("nbHadrons", nbHadrons)
  if not opts.usePT:
    reader.AddSpectator("ptPruned", ptPruned)
  reader.AddSpectator("etaPruned", etaPruned)
  reader.AddSpectator("SubJet_csv", SubJet_csv)
  
  reader.BookMVA("BDTG","weights/inclusive.xml")
  reader.BookMVA("baseline","weights/baseline.xml")
  # reader.BookMVA("subjet","Spring15/ak08_spring15_subjet.weights.xml")


  bdtOuts = []
  bdtOutsBaseline = []
  bdtOutsSubjet = []
  flavours = []
  nbHads = []
  ptPruneds = []
  etaPruneds = []
  massPruneds = []
  SubJet_csvs = []
  
  hBDTGDisc = TH1F("hBDTGDisc","",1000,-5,5)
  hBaselineDisc = TH1F("hBaselineDisc","",1000,-5,5)
  hSubjetDisc = TH1F("hSubjetGDisc","",1000,-5,5)
  

  for jentry in xrange(tree.GetEntries()):

    ientry = tree.LoadTree(jentry)
    nb = tree.GetEntry(jentry)

    for var in varDict:
      if var.find("tau2/tau1") != -1:
        varDict[var][0] = getattr(tree, "tau2")
        varDict[var][0] /= getattr(tree, "tau1")
      else:
        varDict[var][0] = getattr(tree, var)
    
    bdtOutput = reader.EvaluateMVA("BDTG")
    bdtOutputBaseline = reader.EvaluateMVA("baseline")
    # bdtOutputSubjet   = reader.EvaluateMVA("subjet")
    flavour = tree.flavour
    bdtOuts.append(bdtOutput)
    bdtOutsBaseline.append(bdtOutputBaseline)
    # bdtOutsSubjet.append(bdtOutputSubjet)
    flavours.append(flavour)
    nbHads.append(tree.nbHadrons)
    ptPruneds.append(tree.ptPruned)
    etaPruneds.append(tree.etaPruned)
    massPruneds.append(tree.massPruned)
    SubJet_csvs.append(tree.SubJet_csv)
    
    hBDTGDisc.Fill(bdtOutput)
    hBaselineDisc.Fill(bdtOutputBaseline)
    hSubjetDisc.Fill(tree.SubJet_csv)

    if jentry%100000 == 0:
      print jentry, bdtOutput, flavour

  writeSmallTree = True

  if writeSmallTree:
    print "Writing small tree"

    BDTG = array.array('f',[0])
    baseline = array.array('f',[0])
    flav = array.array('f',[0])
    nbHad = array.array('f',[0])
    etaPruned = array.array('f',[0])
    ptPruned = array.array('f',[0])  
    massPruned = array.array('f',[0])
    SubJet_csv = array.array('f',[0])

    fout = TFile('validation/new_validation_%s.root'%(inFileName.replace(".root","")), 'RECREATE')
    outTree = TTree( 'tree', 'b-tagging training tree' )
    outTree.Branch('BDTG', BDTG, 'BDTG/F')
    outTree.Branch('baseline', baseline, 'baseline/F')
    outTree.Branch('flavour', flav, 'flavour/F')
    outTree.Branch('nbHadrons', nbHad, 'nbHadrons/F')
    outTree.Branch('etaPruned', etaPruned, 'etaPruned/F')
    outTree.Branch('ptPruned', ptPruned, 'ptPruned/F')
    outTree.Branch('massPruned', massPruned, 'massPruned/F')
    outTree.Branch('SubJet_csv', SubJet_csv, 'SubJet_csv/F')


    for i in range(len((bdtOuts))):
      BDTG[0] = bdtOuts[i]
      baseline[0] = bdtOutsBaseline[i]
      # subjet[0] = bdtOutsSubjet[i]
      flav[0] = flavours[i]
      nbHad[0] = nbHads[i]
      etaPruned[0] = etaPruneds[i]
      ptPruned[0] = ptPruneds[i]
      massPruned[0] = massPruneds[i]
      SubJet_csv[0] = SubJet_csvs[i]
      if i%10000==0:
        print i, bdtOuts[i], flavours[i]
        print i, bdtOutsBaseline[i], flavours[i]
        # print i, bdtOutsSubjet[i], flavours[i]
      outTree.Fill()
      
      # treeout.Write()
    fout.Write()
    hBDTGDisc.Write()
    hBaselineDisc.Write()
    hSubjetDisc.Write()
    fout.Close()
  print "done", inFileName

def readParallel():

  print "start readParallel()"
  gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()

  inDirName="/shome/thaarres/HiggsTagger/Spring15/"
  files = [ 'rAll_forTraining.root',
           'qcd_forTraining.root'
      ]
  
  # for inFileName in os.listdir(inDirName):
  #  if inFileName.endswith(".root"):
  #    files.append(inFileName)

  # create Pool
  p = multiprocessing.Pool(parallelProcesses)
  print "Using %i parallel processes" %parallelProcesses

  for f in files:
    # debug
    read(inDirName, f)
     # read(f)
    # break
    # run jobs
    #p.apply_async(read, args = (inDirName, f,))

  p.close()
  p.join()



if __name__ == '__main__':
  
    bdtoptions = [ "!H",
                                 "!V",
                                 "NTrees=750",
                                 "MinNodeSize=2.5%",
                                 "BoostType=Grad",
                                 "Shrinkage=0.20",
                                 #"UseBaggedBoost",
                                 #"GradBaggingFraction=0.5",
                                 "nCuts=20",
                                 "MaxDepth=4",
                                 "PruneMethod=CostComplexity",
                                 "PruneStrength=2"
                               ]
 
    # train(bdtoptions)
    # read("/shome/thaarres/HiggsTagger/rootfiles/", "r800_forTraining.root")
    # trainMultiClass()
 #    inDirName="/shome/thaarres/HiggsTagger/Spring15/"
 #    files = [
 #        'r1200_spring15_forTraining.root'
 #        ]
 # #    files = [ "rAll_forTraining.root"]
 # #    files = [ "ttbar_forTraining.root","rAll_forTraining.root",'qcd_forTraining.root']
 #    for f in files:
 #       read(inDirName, f)
    readParallel()

