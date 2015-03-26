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
    "rootfiles/QCD170-300_forTraining.root"	, "rootfiles/QCD300-470_forTraining.root"	,"rootfiles/QCD470-600_forTraining.root","rootfiles/QCD600-800_forTraining.root","rootfiles/QCD800-1000_forTraining.root"	,"rootfiles/QCD1000-1400_forTraining.root"
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
    
  
  treeS.Add('rootfiles/R800_forTraining.root')
  # treeB.Add('QCD1000-1400_forTraining.root')
 #  treeB.Add('QCD170-300_forTraining.root')
 #  treeB.Add('QCD300-470_forTraining.root')
 #  treeB.Add('QCD470-600_forTraining.root')
 #  treeB.Add('QCD600-800_forTraining.root')
 #  treeB.Add('QCD800-1000_forTraining.root')
 #  treeB.Add('QCD1000-1400_forTraining.root')

  
  signal_selection = 'massGroomed>80 && massGroomed<150' # bb
  background_selection = 'massGroomed>80 && massGroomed<150 && fabs(flavour!=5)' # no b
  
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
      # "nTrain_Signal=0::nTest_Signal=12000:nTrain_Background=0:nTest_Background=50000:SplitMode=Random:!V" )
      "nTrain_Signal=30000:nTest_Signal=12000:nTrain_Background=30000:nTest_Background=50000:SplitMode=Random:!V" )
      
  # factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher", "!H:!V:Fisher" )
  factory.BookMethod( ROOT.TMVA.Types.kBDT,
                      "BDTG",
                      # "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedGrad:GradBaggingFraction=0.9:SeparationType=GiniIndex:nCuts=500:NNodesMax=5"
                      ":".join(bdtoptions)
                    )
  
  theCat1Vars =  "massGroomed:tau2/tau1:SV_flight2D_0:SV_flight2D_1:SV_flight2DErr_0:SV_flight2DErr_1:SV_totCharge_0:SV_totCharge_1:SV_mass_0:SV_mass_1:SV_vtx_pt_0:SV_vtx_pt_1:SV_vtx_EnergyRatio_0:SV_vtx_EnergyRatio_1:SV_vtx_deltaR_0:SV_vtx_deltaR_1:trackSip3dSig_3:trackPtRel_3:trackEtaRel_0:trackEtaRel_1:trackEtaRel_2:PFLepton_deltaR:PFLepton_ptrel:PFLepton_ratioRel:PFLepton_IP2D:nSV:SV_nTrk_0:SV_nTrk_1:jetNTracksEtaRel:nSL"
  mcat = factory.BookMethod( ROOT.TMVA.Types.kCategory, "BDTCat","" )
  
  cuts = [
    'abs(etaGroomed)<=1.4 && ptGroomed >= 250 && ptGroomed <500', 'abs(etaGroomed)<=1.4 && ptGroomed >= 500', 'abs(etaGroomed)>1.4 && ptGroomed >= 250 && ptGroomed <500', 'abs(etaGroomed)>1.4 && ptGroomed >= 500'
  ]

  for cut in cuts:
    print "Training in category %s" %cut
    mcat.AddMethod( ROOT.TCut(cut), theCat1Vars, ROOT.TMVA.Types.kBDT, "Category_BDT_1","!H:!V:NTrees=100:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=4" )

  (ROOT.TMVA.gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 2
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
  reader.AddSpectator("ptGroomed",ptGroomed)
  reader.AddSpectator("flavour",flavour)
  reader.AddSpectator("nbHadrons",nbHadrons)

  varDict = {}
  for var in training_vars_float:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])
  for var in training_vars_int:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])

 
  
  reader.BookMVA("BDTG","weights/TMVAClassification_BDTG.weights.xml")

  bdtOuts = []
  flavours = []
  categories = []
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
    # categories.append(tree.vertexCategory)
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
    outTree.Branch('ptGroomed', ptGroomed, 'ptGroomed/F')
    outTree.Branch('etaGroomed', etaGroomed, 'etaGroomed/F')


    for i in range(len((bdtOuts))):
      BDTG[0] = bdtOuts[i]
      flav[0] = flavours[i]
      # cat[0] = categories[i]
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

  inDirName="/shome/thaarres/HiggsTagger/rootfiles/"
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
    # trainMultiClass()
    # readParallel()

