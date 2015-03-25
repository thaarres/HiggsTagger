import ROOT
import os
import multiprocessing
import array

# LR training variables
training_vars_float = [
 "massGroomed",
 "tau2/tau1",
 "SV_flight2D_0",
 "SV_flight2D_1", 
 "SV_flight2DErr_0",
 "SV_flight2DErr_1", 
 "SV_totCharge_0",
 "SV_totCharge_1", 
 "SV_mass_0", 
 "SV_mass_1", 
 "SV_vtx_pt_0",
 "SV_vtx_pt_1",
 "SV_vtx_EnergyRatio_0",
 "SV_vtx_EnergyRatio_1", 
 "SV_vtx_deltaR_0",
 "SV_vtx_deltaR_1", 
 "trackSip3dSig_3", 
 "trackPtRel_3",
 "trackEtaRel_0",
 "trackEtaRel_1",
 "trackEtaRel_2",
 "PFLepton_deltaR",
 "PFLepton_ptrel",
 "PFLepton_ratioRel",
 "PFLepton_IP2D",
  ]

training_vars_int = [
  "nSV",
  "SV_nTrk_0",
  "SV_nTrk_1",
  "jetNTracksEtaRel" ,
  "nSL",
  ]

def train(bdtoptions):
  
  outFile = ROOT.TFile('TMVA_classification.root', 'RECREATE')

  factory = ROOT.TMVA.Factory(
                               "TMVAClassification", 
                               outFile, 
                               "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification"
                             )
  
  TMVA_tools = ROOT.TMVA.Tools.Instance()
  treeS = ROOT.TChain('Fjets')
  treeB = ROOT.TChain('Fjets')
  files = [
    "QCD170-300_forTraining.root"	, "QCD300-470_forTraining.root"	,"QCD470-600_forTraining.root","QCD600-800_forTraining.root","QCD800-1000_forTraining.root"	,"QCD1000-1400_forTraining.root"
  ]
  
  xSec = [12030.,
            7475.,
            587.1,
            167.0,
            28.25,
            8.195,
          ]
          
  genEv = [2001169.,
           1986177.,
           2001071.,
           1997744.,
           1000065.,
           500550.0,
         ]
  
  treelist = []
  for f in files:
    print 'Opening file %s' %f
    file = ROOT.TFile.Open(f)
    tree = file.Get("Fjets")
    treelist.append(tree)
    treeB.Add(f)

  for i in range(0,len(treelist)):
    weight = xSec[i]/genEv[i]
    tree = treelist[i]
    print i
    factory.AddBackgroundTree(tree, weight)
    print 'Setting weight to %f (xSec = %2f, #genevents = %i)' %(weight, xSec[i], genEv[i])
    # tree.SetWeight(weight)
    
  
  treeS.Add('R800_forTraining.root')
  # treeB.Add('QCD1000-1400_forTraining.root')
 #  treeB.Add('QCD170-300_forTraining.root')
 #  treeB.Add('QCD300-470_forTraining.root')
 #  treeB.Add('QCD470-600_forTraining.root')
 #  treeB.Add('QCD600-800_forTraining.root')
 #  treeB.Add('QCD800-1000_forTraining.root')
 #  treeB.Add('QCD1000-1400_forTraining.root')

  
  signal_selection = '' # bb
  background_selection = 'fabs(flavour!=5)' # no b
  
  num_pass = treeS.GetEntries(signal_selection)
  num_fail = treeB.GetEntries(background_selection)

  print 'N events signal', num_pass
  print 'N events background', num_fail
  

  for var in training_vars_float:
    factory.AddVariable(var, 'F') # add float variable
  for var in training_vars_int:
    factory.AddVariable(var, 'I') # add integer variable
   
  factory.AddSpectator("etaGroomed")
  factory.AddSpectator("ptGroomed")
  factory.AddSpectator("flavour")
  factory.AddSpectator("nbHadrons")
   
  factory.SetWeightExpression('1.')

  factory.AddSignalTree(treeS, 1.)
  

  
  factory.PrepareTrainingAndTestTree( ROOT.TCut(signal_selection), ROOT.TCut(background_selection),
                                      "nTrain_Signal=30000:nTest_Signal=12000:nTrain_Background=30000:nTest_Background=50000:SplitMode=Random:!V" )

  factory.BookMethod( ROOT.TMVA.Types.kBDT,
                      "BDTG",
                      # "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedGrad:GradBaggingFraction=0.9:SeparationType=GiniIndex:nCuts=500:NNodesMax=5"
                      ":".join(bdtoptions)
                    )


  # (ROOT.TMVA.gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 2
  factory.TrainAllMethods()

  # factory.OptimizeAllMethods()

  factory.TestAllMethods()

  factory.EvaluateAllMethods()

  outFile.Close()

##   ROOT.gROOT.LoadMacro('$ROOTSYS/tmva/test/TMVAGui.C')
##   ROOT.TMVAGui('TMVA_classification.root')
##   raw_input("Press Enter to continue...")




# # def read(inDirName, inFileName):
# def read(inFileName):
#   print "Reading", inFileName
#   print "################################"
#   print "inFileName is", inFileName
#
#   TMVA_tools = ROOT.TMVA.Tools.Instance()
#
#   tree = ROOT.TChain('btagana/ttree')
#
#   # tree.Add('%s/%s' %(inDirName, inFileName))
#   tree.Add('%s' %(inFileName))
#
#   print "tree is", tree
#   print "################################"
#   print "################################"
#   print "################################"
#   reader = ROOT.TMVA.Reader('TMVAClassification_BDTG')
#
#   varDict = {}
#   for var in training_vars_float:
#     varDict[var] = array.array('f',[0])
#     reader.AddVariable(var, varDict[var])
#   for var in training_vars_int:
#     varDict[var] = array.array('f',[0])
#     reader.AddVariable(var, varDict[var])
#
#
#   reader.BookMVA("BDTG","weights/TMVAClassification_BDTG.weights.xml")
#
#   bdtOuts = []
#   flavours = []
#   categories = []
#   jetPts = []
#   jetEtas = []
#
#   for jentry in xrange(tree.GetEntries()):
#
#     ientry = tree.LoadTree(jentry)
#     nb = tree.GetEntry(jentry)
#
#
#     for var in varDict:
#       print "var = ", var
#       varDict[var][0] = getattr(tree, var)
#
#     print "varDict[var][0] is", varDict[var][0]
#     print "################################"
#     print "################################"
#     print "################################"
#
#     bdtOutput = reader.EvaluateMVA("BDTG")
#     flavour = tree.Jet_flavour
#     bdtOuts.append(bdtOutput)
#     flavours.append(flavour)
#     # categories.append(tree.vertexCategory)
#     jetPts.append(tree.Jet_pt)
#     jetEtas.append(tree.Jet_eta)
#
#     if jentry%10000 == 0:
#       print jentry, bdtOutput, flavour
#
#   writeSmallTree = True
#
#   if writeSmallTree:
#     print "Writing small tree"
#
#     BDTG = array.array('f',[0])
#     flav = array.array('f',[0])
#     # cat = array.array('f',[0])
#     jetPt = array.array('f',[0])
#     jetEta = array.array('f',[0])
#
#     fout = ROOT.TFile('trainPlusBDTG_%s.root'%(inFileName.replace(".root","")), 'RECREATE')
#     outTree = ROOT.TTree( 'tree', 'b-tagging training tree' )
#     outTree.Branch('BDTG', BDTG, 'BDTG/F')
#     outTree.Branch('flavour', flav, 'flavour/F')
#     # outTree.Branch('vertexCategory', cat, 'vertexCategory/F')
#     outTree.Branch('jetPt', jetPt, 'jetPt/F')
#     outTree.Branch('jetEta', jetEta, 'jetEta/F')
#
#
#     for i in range(len((bdtOuts))):
#       BDTG[0] = bdtOuts[i]
#       flav[0] = flavours[i]
#       # cat[0] = categories[i]
#       jetPt[0] = jetPts[i]
#       jetEta[0] = jetEtas[i]
#       if i%10000==0:
#         print i, bdtOuts[i], flavours[i]
#       outTree.Fill()
#       # treeout.Write()
#     fout.Write()
#     fout.Close()
#   print "done", inFileName
# 
# def readParallel():
#
#   print "start readParallel()"
#   ROOT.gROOT.SetBatch(True)
#   parallelProcesses = multiprocessing.cpu_count()
#
#   #inDirName="dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/vlambert/TMVA/ctag_CSVMLP_IVFadapv1/Weighted/"
#  # inDirName="dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Phys14/RSGravitonToWW_kMpl01_M_2000_Tune4C_13TeV_pythia8/"
#   files = [
#    "/shome/thaarres/TMVA_btag/CMSSW_7_3_0/src/RecoBTag/BTagAnalyzerLite/test/Graviton10k.root",
#    "/shome/thaarres/TMVA_btag/CMSSW_7_3_0/src/RecoBTag/BTagAnalyzerLite/test/QCD10k.root"
#     ]
#   #files ["CombinedSVV2NoVertex_B.root"]
#
#   #for inFileName in os.listdir(inDirName):
#   #  if inFileName.endswith(".root") and not (inFileName.find("Eta") >= 0):
#   #    files.append(inFileName)
#
#   # create Pool
#   p = multiprocessing.Pool(parallelProcesses)
#   print "Using %i parallel processes" %parallelProcesses
#
#   for f in files:
#     # debug
#     # read(inDirName, f)
#      read(f)
#     # break
#     # run jobs
#     #p.apply_async(read, args = (inDirName, f,))
#
#   p.close()
#   p.join()
#


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
    # trainMultiClass()
    # readParallel()

