from optparse import OptionParser
import sys
import ConfigParser
import ROOT
import os
import multiprocessing
import array
 
training_vars_float = [
  "PFLepton_ratioRel",
  "z_ratio",
  "tau2IVF/tau1IVF",
  "SV_mass_0",
  "SV_vtx_EnergyRatio_0",
  "SV_vtx_EnergyRatio_1",
  "SV_vtx_deltaR_0", 
  "PFLepton_IP2D"
  # "massGroomed",
#   "tau2/tau1",
#   "SV_flight2D_0",
#   "SV_flight2D_1",
#   "SV_flight2DErr_0",
#   "SV_flight2DErr_1",
#   "SV_totCharge_0",
#   "SV_totCharge_1",
#  "SV_mass_1",
#  "SV_vtx_pt_0",
#  "SV_vtx_pt_1",
#  "SV_vtx_deltaR_1",
#  "trackSip3dSig_3",
#  "trackPtRel_3",
#  "trackEtaRel_0",
#  "trackEtaRel_1",
#  "trackEtaRel_2",
#  "PFLepton_deltaR",
#  "PFLepton_ptrel",
  ]
 
training_vars_int = [
   "nSV",
   "nSL"
  # "SV_nTrk_0",
  # "SV_nTrk_1",
  # "jetNTracksEtaRel" ,
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
                                                                                                                   			      			      			      			      
(opts, args) = parser.parse_args(argv)  

def train(bdtoptions):
  
  outFile = ROOT.TFile('TMVA_unweighted_woPt.root', 'RECREATE')
  print outFile

  factory = ROOT.TMVA.Factory(
                               "TMVAClassification", 
                               outFile, 
                               "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification"
                             )
  
  TMVA_tools = ROOT.TMVA.Tools.Instance()
  treeS = ROOT.TChain('Fjets')
  treeB = ROOT.TChain('Fjets')
  
  
############ OLD LUMI-REWEIGHTING SCHEME!! DO NOT USE! Reweight before passing ############
# files = [
#     "weighted_rootfiles/QCD170-300_forTraining.root"  , "weighted_rootfiles/QCD300-470_forTraining.root"  ,"weighted_rootfiles/QCD470-600_forTraining.root","weighted_rootfiles/QCD600-800_forTraining.root","weighted_rootfiles/QCD800-1000_forTraining.root"  ,"weighted_rootfiles/QCD1000-1400_forTraining.root","weighted_rootfiles/QCD1400-1800_forTraining.root"
#   ]
#
#   xSec = [12030.,
#             7475.,
#             587.1,
#             167.0,
#             28.25,
#             8.195,
#             0.7346
#           ]
#   genEv = [2001169.,
#            1986177.,
#            2001071.,
#            1997744.,
#            1000065.,
#            500550.0,
#            199627.0,
#          ]
#
#   treelist = []
#   for f in files:
#     print 'Opening file %s' %f
#     file = ROOT.TFile.Open(f)
#     tree = file.Get("Fjets")
#     treelist.append(tree)
#     treeB.Add(f)
#
#   for i in range(0,len(treelist)):
#     weight = xSec[i]/genEv[i]
#     tree = treelist[i]
#     print i
#     factory.AddBackgroundTree(tree, weight)
#     print 'Setting weight to %f (xSec = %2f, #genevents = %i)' %(weight, xSec[i], genEv[i])
#     # tree.SetWeight(weight)

 #  treeB.Add('QCD1000-1400_forTraining.root')
 #  treeB.Add('QCD170-300_forTraining.root')
 #  treeB.Add('QCD300-470_forTraining.root')
 #  treeB.Add('QCD470-600_forTraining.root')
 #  treeB.Add('QCD600-800_forTraining.root')
 #  treeB.Add('QCD800-1000_forTraining.root')
 #  treeB.Add('QCD1000-1400_forTraining.root')

  
  treeS.Add('weighted_rootfiles/r800_forTraining.root')
  # treeS.Add('weighted_rootfiles/r1000_forTraining.root')
#   treeS.Add('weighted_rootfiles/r1600_forTraining.root')
#   treeS.Add('weighted_rootfiles/r2000_forTraining.root')
  treeB.Add('weighted_rootfiles/qcd_forTraining.root')
  
  signal_selection = 'massGroomed>80 && massGroomed<150' # bb
  print "Signal selection = %s" %signal_selection
  if(opts.gluonsplitting):
    background_selection = 'massGroomed>80 && massGroomed<150 && abs(flavour==5) && nbHadrons>1' # gsp
  elif(opts.charm):
    background_selection = 'massGroomed>80 && massGroomed<150 && abs(flavour==4)' # charm
  else:
    background_selection = 'massGroomed>80 && massGroomed<150 && abs(flavour!=5)' # no b
  
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
    factory.AddVariable("ptGroomed", 'F')
    
  factory.AddSpectator("massGroomed")
  factory.AddSpectator("etaGroomed")
  factory.AddSpectator("flavour")
  factory.AddSpectator("nbHadrons")
  
  if not opts.usePT: 
     factory.AddSpectator("ptGroomed")
    
  if (opts.weight):
    # factory.AddSpectator("weight_etaPt")
    factory.SetWeightExpression('weight_etaPt')
  else:
    factory.SetWeightExpression('1.')
    
  factory.AddSignalTree(treeS, 1.)
  factory.AddBackgroundTree(treeB, 1.)

  
  factory.PrepareTrainingAndTestTree( ROOT.TCut(signal_selection), ROOT.TCut(background_selection), 
      "nTrain_Signal=0::nTest_Signal=0:nTrain_Background=0:nTest_Background=0:SplitMode=Random:!V" )
      # "nTrain_Signal=30000:nTest_Signal=12000:nTrain_Background=30000:nTest_Background=50000:SplitMode=Random:!V" )
      
  # factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher", "!H:!V:Fisher" )
  factory.BookMethod( ROOT.TMVA.Types.kBDT,
                      "BDTG",
                      # "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedGrad:GradBaggingFraction=0.9:SeparationType=GiniIndex:nCuts=500:NNodesMax=5"
                      ":".join(bdtoptions)
                    )
  
  if (opts.categories):
    
    if(opts.usePT):  
      theCat1Vars = "PFLepton_ratioRel:z_ratio:tau2IVF/tau1IVF:SV_mass_0:SV_vtx_EnergyRatio_0:SV_vtx_EnergyRatio_1:SV_vtx_deltaR_0:PFLepton_IP2D:nSV:nSL:ptGroomed"
    else:
      theCat1Vars = "PFLepton_ratioRel:z_ratio:tau2IVF/tau1IVF:SV_mass_0:SV_vtx_EnergyRatio_0:SV_vtx_EnergyRatio_1:SV_vtx_deltaR_0:PFLepton_IP2D:nSV:nSL"
    # theCat1Vars =  "massGroomed:tau2/tau1:SV_flight2D_0:SV_flight2D_1:SV_flight2DErr_0:SV_flight2DErr_1:SV_totCharge_0:SV_totCharge_1:SV_mass_0:SV_mass_1:SV_vtx_pt_0:SV_vtx_pt_1:SV_vtx_EnergyRatio_0:SV_vtx_EnergyRatio_1:SV_vtx_deltaR_0:SV_vtx_deltaR_1:trackSip3dSig_3:trackPtRel_3:trackEtaRel_0:trackEtaRel_1:trackEtaRel_2:PFLepton_deltaR:PFLepton_ptrel:PFLepton_ratioRel:PFLepton_IP2D:nSV:SV_nTrk_0:SV_nTrk_1:jetNTracksEtaRel:nSL"
    mcat = factory.BookMethod( ROOT.TMVA.Types.kCategory, "BDTCat4","" )  
    cuts = [
      'abs(etaGroomed)<=1.4 && ptGroomed < 400', 'abs(etaGroomed)<=1.4 && ptGroomed >= 400', 'abs(etaGroomed)>1.4 &&  ptGroomed <400', 'abs(etaGroomed)>1.4 && ptGroomed >= 400'
    ]
    
    for cut in cuts:
      print "Training in category %s" %cut                                               
      mcat.AddMethod( ROOT.TCut(cut), theCat1Vars, ROOT.TMVA.Types.kBDT, "Category_BDT_4","!H:!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=4" )
    
    mcat2 = factory.BookMethod( ROOT.TMVA.Types.kCategory, "BDTCat12","" )  
    cuts2 = [
      'abs(etaGroomed)<=1.2 && ptGroomed <400', 'abs(etaGroomed)<=1.2 && ptGroomed >= 400 && ptGroomed < 600', 'abs(etaGroomed)<=1.2 && ptGroomed >= 600 && ptGroomed < 800', 'abs(etaGroomed)<=1.2 && ptGroomed >= 800',
      'abs(etaGroomed)>1.2 && abs(etaGroomed)<=2.1 && ptGroomed < 400', 'abs(etaGroomed)>1.2 && abs(etaGroomed)<=2.1 && ptGroomed >= 400 && ptGroomed < 600', 'abs(etaGroomed)>1.2 && abs(etaGroomed)<=2.1 && ptGroomed >= 600 && ptGroomed < 800', 'abs(etaGroomed)>1.2 && abs(etaGroomed)<=2.1 && ptGroomed >= 800',
      'abs(etaGroomed)>2.1 && ptGroomed <400', 'abs(etaGroomed)>2.1 && ptGroomed >= 400 && ptGroomed < 600', 'abs(etaGroomed)>2.1 && ptGroomed >= 600 && ptGroomed < 800','abs(etaGroomed)>2.1 && ptGroomed > 800'
    ]
 
    for cut in cuts2:
      print "Training in category %s" %cut
      mcat2.AddMethod( ROOT.TCut(cut), theCat1Vars, ROOT.TMVA.Types.kBDT, "Category_BDT_12","!H:!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=4" )
  
  
  # (ROOT.TMVA.gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 2
  factory.TrainAllMethods()
  # factory.OptimizeAllMethods()

  factory.TestAllMethods()

  factory.EvaluateAllMethods()

  outFile.Close()

  # ROOT.gROOT.LoadMacro('$ROOTSYS/tmva/test/TMVAGui.C')
  # ROOT.TMVAGui('TMVA_classification.root')
  # raw_input("Press Enter to continue...")

# # def read(inDirName, inFileName):
def read(inDirName, inFileName):
  print "Reading", inFileName
  print "################################"
  print "inFileName is", inFileName

  TMVA_tools = ROOT.TMVA.Tools.Instance()

  tree = ROOT.TChain('Fjets')
  tree.Add('%s%s' %(inDirName,inFileName))
  print '%s%s' %(inDirName,inFileName)
  print "tree is", tree
  print "################################"
  print "################################"
  print "################################"
  reader = ROOT.TMVA.Reader('TMVAClassification_BDTG')
  
  etaGroomed = array.array('f',[0])
  ptGroomed = array.array('f',[0])
  flavour = array.array('f',[0])
  nbHadrons = array.array('f',[0])
  reader.AddSpectator("etaGroomed",etaGroomed)
  reader.AddSpectator("flavour",flavour)
  reader.AddSpectator("nbHadrons",nbHadrons)
  factory.AddSpectator("massGroomed")
  if not opts.usePT:
    reader.AddSpectator("ptGroomed",ptGroomed)

  varDict = {}
  for var in training_vars_float:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])
  for var in training_vars_int:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])
  if(opts.usePT):
    reader.AddVariable("ptGroomed",ptGroomed)
  
 
  
  reader.BookMVA("BDTG","weights/TMVAClassification_BDTG.weights.xml")

  bdtOuts = []
  flavours = []
  ptGroomeds = []
  etaGroomeds = []

  for jentry in xrange(tree.GetEntries()):

    ientry = tree.LoadTree(jentry)
    nb = tree.GetEntry(jentry)


    # for var in varDict:
#       print "var = ", var
#       varDict[var][0] = getattr(tree, var)

    # print "varDict[var][0] is", varDict[var][0]
 #    print "################################"
 #    print "################################"
 #    print "################################"

    bdtOutput = reader.EvaluateMVA("BDTG")
    flavour = tree.flavour
    bdtOuts.append(bdtOutput)
    flavours.append(flavour)
    ptGroomeds.append(tree.ptGroomed)
    etaGroomeds.append(tree.etaGroomed)

    if jentry%10000 == 0:
      print jentry, bdtOutput, flavour

  writeSmallTree = True

  if writeSmallTree:
    print "Writing small tree"

    BDTG = array.array('f',[0])
    flav = array.array('f',[0])

    jetPt = array.array('f',[0])
    jetEta = array.array('f',[0])

    fout = ROOT.TFile('trainPlusBDTG_%s.root'%(inFileName.replace(".root","")), 'RECREATE')
    outTree = ROOT.TTree( 'tree', 'b-tagging training tree' )
    outTree.Branch('BDTG', BDTG, 'BDTG/F')
    outTree.Branch('flavour', flav, 'flavour/F')
    if(opts.usePT):
      outTree.Branch('ptGroomed', ptGroomed, 'ptGroomed/F')
    outTree.Branch('etaGroomed', etaGroomed, 'etaGroomed/F')


    for i in range(len((bdtOuts))):
      BDTG[0] = bdtOuts[i]
      flav[0] = flavours[i]
      ptGroomed[0] = ptGroomeds[i]
      etaGroomed[0] = etaGroomeds[i]
      if i%10000==0:
        print i, bdtOuts[i], flavours[i]
      outTree.Fill()
      # treeout.Write()
    fout.Write()
    fout.Close()
  print "done", inFileName

def readParallel():

  print "start readParallel()"
  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()

  inDirName="/shome/thaarres/HiggsTagger/weighted_rootfiles/"
  files = [
    'R800_forTraining.root',
#     'QCD1000-1400_forTraining.root',
#     'QCD120-170_forTraining.root',
#     'QCD1400-1800_forTraining.root',
#     'QCD170-300_forTraining.root',
#     'QCD300-470_forTraining.root',
#     'QCD470-600_forTraining.root',
#     'QCD600-800_forTraining.root',
#     'QCD800-1000_forTraining.root',
    ]
  
  for inFileName in os.listdir(inDirName):
   if inFileName.endswith(".root"):
     files.append(inFileName)

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
                                 "NTrees=100",
                                 "MinNodeSize=1.5%",
                                 "BoostType=Grad",
                                 "Shrinkage=0.10",
                                 "UseBaggedBoost",
                                 "GradBaggingFraction=0.5",
                                 "nCuts=20",
                                 "MaxDepth=4",
                               ]
    train(bdtoptions)
    read("/shome/thaarres/HiggsTagger/rootfiles/signal/", "r1000_forTraining.root")
    # trainMultiClass()
    # readParallel()

