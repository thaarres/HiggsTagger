from ROOT import *

def getPerformanceCurve(fFileS1, fFileB1, fPlotS1, fPlotB1, fXMin=0, fXMax=0):
  file_S1 = TFile(fFileS1)
  file_B1 = TFile(fFileB1)

  inclusive_S = file_S1.Get("hBDTGDisc")
  inclusive_B = file_B1.Get("hBDTGDisc")
    
  subjet_S = file_S1.Get('hSubjetGDisc')
  subjet_B = file_B1.Get('hSubjetGDisc')
    
  baseline_S = file_S1.Get('hBaselineDisc')
  baseline_B = file_B1.Get('hBaselineDisc')

  inclusive_cut = 0
  subjet_cut  = 0
  baseline_cut = 0
    
  print "############## INCLUSIVE ##############"
    #total jet count for denominator of efficiency calculation
  denom_S_1 = float( inclusive_S.Integral() )
  denom_B_1 = float( inclusive_B.Integral(0,inclusive_B.GetNbinsX()) )    
  print "BKG denominator %f" %denom_B_1
  for i in range(0 ,inclusive_B.GetNbinsX()):
    integral = inclusive_B.Integral(0,i)
    if(denom_B_1*0.19 <= integral <= denom_B_1*0.21):
      inclusive_cut = inclusive_B.GetXaxis().GetBinCenter(i)
      print "For %s: at 20 percent mistag rate, cut is %f "%(fPlotS1, inclusive_cut )
      break
  print "############## SUBJET ##############"
    #total jet count for denominator of efficiency calculation
  denom_S_1 = float( subjet_S.Integral() )
  denom_B_1 = float( subjet_B.Integral(0,subjet_B.GetNbinsX()) )
  print "BKG denominator %f" %denom_B_1
  for i in range(0 ,subjet_B.GetNbinsX()):
    integral = subjet_B.Integral(0,i)
    if(denom_B_1*0.18 <= integral <= denom_B_1*0.22):
      subjet_cut = subjet_B.GetXaxis().GetBinCenter(i)
      print "For %s: at 20 percent mistag rate, cut is %f "%(fPlotS1, subjet_cut )
      break
  print "############## BASELINE ##############"
    #total jet count for denominator of efficiency calculation
  denom_S_1 = float( baseline_S.Integral() )
  denom_B_1 = float( baseline_B.Integral(0,baseline_B.GetNbinsX()) )
  print "BKG denominator %f" %denom_B_1
  for i in range(0 ,baseline_B.GetNbinsX()):
    integral = baseline_B.Integral(0,i)
    if(denom_B_1*0.19 <= integral <= denom_B_1*0.21):
      baseline_cut = baseline_B.GetXaxis().GetBinCenter(i)
      print "For %s: at 20 percent mistag rate, cut is %f "%(fPlotS1, baseline_cut )
      break

  h2_S_new = TH1F("hBDTGDisc_S","",200,0.,1.)
  h2_B_new = TH1F("hBDTGDisc_B","",200,0.,1.)
  h2_S_baseline = TH1F("hBaselineDisc_S","",200,0.,1.)
  h2_B_baseline = TH1F("hBaselineDisc_B","",200,0.,1.)
  h2_S_subjet = TH1F("hSubjetDisc_S","",200,0.,1.)
  h2_B_subjet = TH1F("hSubjetDisc_B","",200,0.,1.)

  tau21_new = TH1F("S_bin1","",200,0.,1.)
  tau21_baseline = TH1F("S_bin2","",200,0.,1.)
  tau21_subjet = TH1F("S_bin3","",200,0.,1.)




  treeS=file_S1.Get('tree') 
  treeB=file_B1.Get('tree') 
  Sentry = treeS.GetEntries() 
  Bentry = treeB.GetEntries() 
   
  histos = []
  
  print "Inclusive = %f" %inclusive_cut
  print "Subjet = %f" %subjet_cut
  print "baseline = %f" %baseline_cut

  for event in treeS:
     # if (abs(event.flavour)==5 and event.nbHadrons>1 and event.ptPruned > pTmin and event.ptPruned <= pTmax):
     
       #h2_S_baseline.Fill( event.massPruned )
       h2_S_baseline.Fill( (event.tau2/event.tau1) )
       if (event.baseline > baseline_cut):
         #tau21_baseline.Fill( event.massPruned )
         tau21_baseline.Fill( (event.tau2/event.tau1) )
         
     
       #h2_S_subjet.Fill( event.massPruned )
       h2_S_subjet.Fill( (event.tau2/event.tau1) )
       if (event.SubJet_csv > subjet_cut):
         #tau21_subjet.Fill( event.massPruned )
         tau21_subjet.Fill( (event.tau2/event.tau1) )
       #h2_S_new.Fill( event.massPruned )
       h2_S_new.Fill( (event.tau2/event.tau1) )
       if (event.BDTG > inclusive_cut):
         #tau21_new.Fill( event.massPruned )
         tau21_new.Fill( (event.tau2/event.tau1) )

  h2_S_baseline.Scale(1./h2_S_baseline.Integral())
  tau21_baseline.Scale(1./tau21_baseline.Integral())
  h2_S_subjet.Scale(1./h2_S_subjet.Integral())
  tau21_subjet.Scale(1./tau21_subjet.Integral())
  h2_S_new.Scale(1./h2_S_new.Integral())
  tau21_new.Scale(1./tau21_new.Integral())
  
  
  h2_S_baseline.SetLineColor(kGreen+2)
  tau21_baseline.SetLineColor(kRed)
  h2_S_subjet.SetLineColor(kBlue)
  tau21_subjet.SetLineColor(kBlack)
  h2_S_new.SetLineColor(kMagenta)
  tau21_new.SetLineColor(kOrange+2)
  
  histos.append(h2_S_baseline)
  histos.append(tau21_baseline)
  histos.append(h2_S_subjet)
  histos.append(tau21_subjet)
  histos.append(h2_S_new)
  histos.append(tau21_new)
  
  c = TCanvas("c", "",800,800)
  c.cd()
  h2_S_baseline.Draw("hist")
  tau21_baseline.Draw("histSAME")
  h2_S_subjet.Draw("histSAME")
  tau21_subjet.Draw("histSAME")
  h2_S_new.Draw("histSAME")
  tau21_new.Draw("histSAME")
  h2_S_baseline.SetTitleOffset(1.2,"X")
  h2_S_baseline.SetTitleOffset(1.5,"Y")
  c.SetGridx()
  c.SetGridy()
  
  h2_S_baseline.GetXaxis().SetTitle('#tau_{21}')
  h2_S_baseline.GetYaxis().SetTitle("A.U")
  h2_S_baseline.SetTitleOffset(1.2,"X")
  h2_S_baseline.SetTitleOffset(1.5,"Y")

  legend = TLegend(.11,.6,.36,.77)
  legend.SetBorderSize(0)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetTextFont(42)
  legend.SetTextSize(0.021)
  legend.AddEntry(h2_S_baseline,"Baseline: All","l") 
  legend.AddEntry(tau21_baseline,"Baseline: After discr. cut","l") 
  legend.AddEntry(h2_S_subjet,"Subjet CSV: All","l") 
  legend.AddEntry(tau21_subjet,"Subjet CSV: After discr. cut","l") 
  legend.AddEntry(h2_S_new,"Inclusive: All","l") 
  legend.AddEntry(tau21_new,"Inclusive: After discr. cut","l") 

  legend.Draw()
  l1 = TLatex()
  l1.SetTextAlign(13)
  l1.SetTextFont(42)
  l1.SetNDC()
  l1.SetTextSize(0.04)

  l1.SetTextAlign(12)
  l1.SetTextSize(0.045)
  l1.SetTextFont(62)
  l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

  l1.SetTextFont(42)
  l1.SetTextSize(0.025)


  c.SaveAs('tau21.root')
  

  
  
   # for event in treeB:
   #   if (abs(event.flavour)==5 and event.nbHadrons>1 and event.ptPruned > pTmin and event.ptPruned <= pTmax and ((event.tau2/event.tau1) < 0.4 ) ):
   #     # h2_B_baseline.Fill( event.baseline )
   #     h2_B_subjet.Fill( event.SubJet_csv )
   #     h2_B_new.Fill( event.BDTG )
   #     if( (event.tau2/event.tau1) < 0.4 ):
   #       B_bin1.Fill( event.BDTG )
   #       B_bin1_subjet.Fill( event.SubJet_csv )


  return histos

def formatGraph(graph, graphNum):
    colors = [ kGreen+2, kRed, kBlue, kBlack, kMagenta, kOrange+2, kCyan ]
    graphColor = colors[graphNum % 7]
    lineStyle = (graphNum % 11) + 1
    graph.SetLineColor(graphColor)
    graph.SetLineStyle(lineStyle)
    graph.SetLineWidth(2)

def plotPerformanceCurves(graphs, ordering, fTitle, fXAxisTitle, fYAxisTitle, fExtraInfo, fOutputFile, fXmin, fXmax, fYmin, fYmax, fLogy=0):

    gROOT.SetBatch(kTRUE)
    gStyle.SetGridColor(kGray)
    gStyle.SetOptStat(kFALSE)
    gStyle.SetPadTopMargin(0.07)
    gStyle.SetPadBottomMargin(0.13)
    gStyle.SetPadLeftMargin(0.14)
    gStyle.SetPadRightMargin(0.06)
    gROOT.ForceStyle()

    c = TCanvas("c", "",800,800)
    c.cd()
    bkg = TH2D("bkg","",100,fXmin,fXmax,100,fYmin,fYmax)
    bkg.GetXaxis().SetTitle(fXAxisTitle)
    bkg.GetYaxis().SetTitle(fYAxisTitle)
    bkg.SetTitleOffset(1.2,"X")
    bkg.SetTitleOffset(1.5,"Y")
    bkg.Draw()
    c.SetGridx()
    c.SetGridy()

    legend = TLegend(.16,.64,.36,.77)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.021)

    graphCounter = 0
    for g in range(0,len(graphs)):
        graph = graphs[g]
        legend.AddEntry(graph, ordering[g],"l")
        formatGraph(graph,graphCounter)
        graph.Draw("histSAME")
        graphCounter += 1

    if (fLogy):
        c.SetLogy()
    legend.Draw()
    l1 = TLatex()
    l1.SetTextAlign(13)
    l1.SetTextFont(42)
    l1.SetNDC()
    l1.SetTextSize(0.04)
    l1.DrawLatex(0.14+0.03,0.85, fTitle)

    l1.SetTextAlign(12)
    l1.SetTextSize(0.045)
    l1.SetTextFont(62)
    l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

    l1.SetTextFont(42)
    l1.SetTextSize(0.025)
    l1.DrawLatex(0.2,0.42, fExtraInfo)

    c.SaveAs(fOutputFile)


def makePlots():
    # for multiple plots on the same canvas

    #-------------------------------
    # # BB vs GSP: r800 validation
    ordering = [] # vectors storing the order of legend entries
    mg = [] # maps to hold legend entries and TGraph*s

    # graphMap["All_reweighted_r800"]    = getPerformanceCurve("tmp_reweighted_r800/validation2_r800_forTraining.root","tmp_reweighted_r800/validation2_qcd_forTraining.root","hBDTGDisc","hBDTGDisc")
    
    mg = getPerformanceCurve("validation/tau21_validation_rAll_forTraining.root","validation/tau21_validation_qcd_forTraining.root","hBDTGDisc","hBDTGDisc")

    ordering.append("Baseline: All")
    ordering.append("Baseline: After discr. cut")
    ordering.append("Subjet CSV: All")
    ordering.append("Subjet CSV: After discr. cut")
    ordering.append("Inclusive: All")
    ordering.append("Inclusive: After discr. cut")
    #
    plotPerformanceCurves(mg,ordering,"","M_{pruned}","Arbitrary units","70 GeV < M_{p} < 200 GeV , p_{T} > 300 GeV","tmvacomp.pdf",0, 1, 1E-3, 1, 0)

    #-------------------------------
    
    # #-------------------------------
    # BB vs GSP: r2000 validation
    # ordering = [] # vectors storing the order of legend entries
 #    graphMap = {} # maps to hold legend entries and TGraph*s
 #
 #    graphMap["Baseline"]   = getPerformanceCurve("tmp_reweighted_r800/validation2_r2000_forTraining.root","tmp_reweighted_r800/validation2_qcd_forTraining.root","hBDTCat8Disc","hBDTCat8Disc")
 #    graphMap["Subjet CSV"]   = getPerformanceCurve("tmp_unweighted_r800/validation2_r2000_forTraining.root","tmp_unweighted_r800/validation2_qcd_forTraining.root","hBDTCat8Disc","hBDTCat8Disc")
 #    graphMap["Inclusive training"]   = getPerformanceCurve("tmp_reweighted_rALL/validation_r2000_forTraining.root","tmp_reweighted_rALL/validation_qcd_forTraining.root","hBDTCat8Disc","hBDTCat8Disc")
 #    graphMap["All (unweighted)"]   = getPerformanceCurve("tmp_unweighted_rALL/validation_r2000_forTraining.root","tmp_unweighted_rALL/validation_qcd_forTraining.root","hBDTCat8Disc","hBDTCat8Disc")
 #
 #    ordering.append("Baseline")
 #    ordering.append("Subjet CSV")
 #    ordering.append("Inclusive training")
 #    ordering.append("All (unweighted)")
 #
 #    plotPerformanceCurves(graphMap,ordering,"R=(2.0 TeV)","Tagging efficiency (H#rightarrowb#bar{b})","1 - mistagging efficiency (g#rightarrowb#bar{b})","70 GeV < M_{p} < 200 GeV , p_{T} > 300 GeV","tmvacomp_r2000validation.pdf",0, 1, 1E-3, 1, 0)
 #

if __name__ == "__main__":
    makePlots()
