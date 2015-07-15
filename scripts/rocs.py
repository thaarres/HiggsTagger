from ROOT import *
import math

def getPerformanceCurve(fFileS1, fFileB1, pTmin, pTmax, fXMin=0, fXMax=0):
    #get files and histograms
    file_S1 = TFile(fFileS1)
    file_B1 = TFile(fFileB1)
    
    # h2_S_new = file_S1.Get(fPlotS1)
    # h2_B_new = file_B1.Get(fPlotB1)
    
    h2_S_new = TH1F("hBDTGDisc_S","",1000,-5.,5.)
    h2_B_new = TH1F("hBDTGDisc_B","",1000,-5.,5.)
    h2_S_baseline = TH1F("hBaselineDisc_S","",1000,-5.,5.)
    h2_B_baseline = TH1F("hBaselineDisc_B","",1000,-5.,5.)
    h2_S_subjet = TH1F("hSubjetDisc_S","",1000,-5.,5.)
    h2_B_subjet = TH1F("hSubjetDisc_B","",1000,-5.,5.)
    
    S_bin1 = TH1F("S_bin1","",1000,-5.,5.)
    S_bin2 = TH1F("S_bin2","",1000,-5.,5.)
    S_bin3 = TH1F("S_bin3","",1000,-5.,5.)
    B_bin1 = TH1F("B_bin1","",1000,-5.,5.)
    B_bin2 = TH1F("B_bin2","",1000,-5.,5.)
    B_bin3 = TH1F("B_bin3","",1000,-5.,5.)
    #
    # S_bin1_subjet = TH1F("S_bin1_subjet","",1000,-5.,5.)
    # S_bin2_subjet = TH1F("S_bin2_subjet","",1000,-5.,5.)
    # S_bin3_subjet = TH1F("S_bin3_subjet","",1000,-5.,5.)
    # B_bin1_subjet = TH1F("B_bin1_subjet","",1000,-5.,5.)
    # B_bin2_subjet = TH1F("B_bin2_subjet","",1000,-5.,5.)
    # B_bin3_subjet = TH1F("B_bin3_subjet","",1000,-5.,5.)
    # S_bin1_baseline = TH1F("S_bin1_baseline","",1000,-5.,5.)
    # B_bin1_baseline = TH1F("B_bin1_baseline","",1000,-5.,5.)

    
    
    treeS=file_S1.Get('tree') 
    treeB=file_B1.Get('tree') 
    Sentry = treeS.GetEntries() 
    Bentry = treeB.GetEntries() 

    for event in treeS:
      if(5. < event.SubJet_csv < -5.):
        subjetcsv = -1.
      else:
        subjetcsv = event.SubJet_csv  
      if(5. < event.BDTG < -5.):
        BDTG = -1.
      else:
        BDTG = event.BDTG  
      # if (abs(event.flavour)==5 and event.nbHadrons>1 and event.ptPruned > pTmin and event.ptPruned <= pTmax):
      if (event.ptPruned > pTmin and event.ptPruned <= pTmax):
        # h2_S_baseline.Fill( event.baseline )
        h2_S_subjet.Fill( subjetcsv )
        h2_S_new.Fill( BDTG )
        # if( (event.tau2/event.tau1) < 0.4 ):
        #   S_bin1.Fill( event.BDTG )
        #   S_bin1_subjet.Fill( subjetcsv )
        #   S_bin1_baseline.Fill( event.baseline )
        if (event.ptPruned > 300. and event.ptPruned <= 470.):
          S_bin1.Fill( BDTG )
          # S_bin1_subjet.Fill( event.SubJet_csv )
        if (event.ptPruned > 470. and event.ptPruned <= 600.):
          S_bin2.Fill( BDTG )
          # S_bin2_subjet.Fill( event.SubJet_csv )
        if (event.ptPruned > 600. and event.ptPruned <= 2000.):
          S_bin3.Fill( BDTG )
          # S_bin3_subjet.Fill( event.SubJet_csv )
    
    for event in treeB:
      if(event.SubJet_csv < -5):
        subjetcsv = -1.
      else:
        subjetcsv = event.SubJet_csv
      if(5. < event.BDTG < -5.):
        BDTG = -1.
      else:
        BDTG = event.BDTG  
      if (abs(event.flavour)==5 and event.nbHadrons>1 and event.ptPruned > pTmin and event.ptPruned <= pTmax):
        # h2_B_baseline.Fill( event.baseline )
        h2_B_subjet.Fill( subjetcsv )
        h2_B_new.Fill( BDTG )
        # if( (event.tau2/event.tau1) < 0.4 ):
        #   B_bin1.Fill( event.BDTG )
        #   B_bin1_subjet.Fill( subjetcsv )
        #   B_bin1_baseline.Fill( event.baseline )
        if (event.ptPruned > 300. and event.ptPruned <= 470.):
          B_bin1.Fill( BDTG )
        if (event.ptPruned > 470. and event.ptPruned <= 600.):
          B_bin2.Fill( BDTG )
          # B_bin2_subjet.Fill( event.SubJet_csv )
        if (event.ptPruned > 600. and event.ptPruned <= 2000.):
          B_bin3.Fill( BDTG )
          # B_bin3_subjet.Fill( event.SubJet_csv )
    
    
    
    
    mg = []    

    #total jet count for denominator of efficiency calculation
    denom_S_all = float( h2_S_new.Integral(380,610) )
    denom_B_all = float( h2_B_new.Integral(380,610) )
    
    denom_S_bin3 = float( S_bin3.Integral(380,610) )
    denom_B_bin3 = float( B_bin3.Integral(380,610) )
    
    denom_S_bin2 = float( S_bin2.Integral(380,610) )
    denom_B_bin2 = float( B_bin2.Integral(380,610) )
    
    denom_S_bin1 = float( S_bin1.Integral(380,610) )
    denom_B_bin1 = float( B_bin1.Integral(380,610) )
    
    g_new = TGraph(49)

    for i in range(5):
        num_S_new = float( h2_S_new.Integral(602-i,602) )
        num_B_new = float( h2_B_new.Integral(602-i,602) )
        g_new.SetPoint( i,(num_S_new/denom_S_all),1-(num_B_new/denom_B_all) )
        # g_new.SetPoint( i,(num_B_new/denom_B_all),(num_S_new/denom_S_all) )

    for i in range(1,40):
        num_S_new = float( h2_S_new.Integral(602-(i*5),602) )
        num_B_new = float( h2_B_new.Integral(602-(i*5),602) )
        g_new.SetPoint( i+4,(num_S_new/denom_S_all),1-(num_B_new/denom_B_all) )
        # g_eff_4.SetPoint(i+4,(num_B_new/denom_B_all),(num_S_new/denom_S_all) )
    for i in range(1,6):
        num_S_new = float( h2_S_new.Integral(407-i,602) )
        num_B_new = float( h2_B_new.Integral(407-i,602) )
        g_new.SetPoint(i+43,(num_S_new/denom_S_all),1-(num_B_new/denom_B_all))
        # g_new.SetPoint(i+43,(num_B_new/denom_B_all),(num_S_new/denom_S_all) )
    

    
    g1 = TGraph(49)
    for i in range(5):
        num_S = float( S_bin1.Integral(602-i,602) )
        num_B = float( B_bin1.Integral(602-i,602) )
        g1.SetPoint( i,(num_S/denom_S_bin1),1-(num_B/denom_B_bin1) )
        # g1.SetPoint( i,(num_B/denom_B_bin1),(num_S/denom_S_bin1) )

    for i in range(1,40):
        num_S = float( S_bin1.Integral(602-(i*5),602) )
        num_B = float( B_bin1.Integral(602-(i*5),602) )
        g1.SetPoint( i+4,(num_S/denom_S_bin1),1-(num_B/denom_B_bin1) )
        # g1.SetPoint(i+4,(num_B/denom_B_bin1),(num_S/denom_S_bin1) )
    for i in range(1,6):
        num_S = float( S_bin1.Integral(407-i,602) )
        num_B = float( B_bin1.Integral(407-i,602) )
        g1.SetPoint(i+43,(num_S/denom_S_bin1),1-(num_B/denom_B_bin1))
       # g1.SetPoint(i+43,(num_B/denom_B_bin1),(num_S/denom_S_bin1) )
   

    g2 = TGraph(49)
    for i in range(5):
        num_S = float( S_bin2.Integral(602-i,602) )
        num_B = float( B_bin2.Integral(602-i,602) )
        g2.SetPoint( i,(num_S/denom_S_bin2),1-(num_B/denom_B_bin2) )
        # g1.SetPoint( i,(num_B/denom_B_bin2),(num_S/denom_S_bin2) )

    for i in range(1,40):
        num_S = float( S_bin2.Integral(602-(i*5),602) )
        num_B = float( B_bin2.Integral(602-(i*5),602) )
        g2.SetPoint( i+4,(num_S/denom_S_bin2),1-(num_B/denom_B_bin2) )
        # g1.SetPoint(i+4,(num_B/denom_B_bin2),(num_S/denom_S_bin2) )
    for i in range(1,6):
        num_S = float( S_bin2.Integral(407-i,602) )
        num_B = float( B_bin2.Integral(407-i,602) )
        g2.SetPoint(i+43,(num_S/denom_S_bin2),1-(num_B/denom_B_bin2))
        # g_new.SetPoint(i+43,(num_B/denom_B_bin2),(num_S/denom_S_bin2) )



    g3 = TGraph(49)
    for i in range(5):
        num_S = float( S_bin3.Integral(602-i,602) )
        num_B = float( B_bin3.Integral(602-i,602) )
        g3.SetPoint( i,(num_S/denom_S_bin3),1-(num_B/denom_B_bin3) )
        # g3.SetPoint( i,(num_B/denom_B_bin3),(num_S/denom_S_bin3) )

    for i in range(1,40):
        num_S = float( S_bin3.Integral(602-(i*5),602) )
        num_B = float( B_bin3.Integral(602-(i*5),602) )
        g3.SetPoint( i+4,(num_S/denom_S_bin3),1-(num_B/denom_B_bin3) )
        # g3.SetPoint(i+4,(num_B/denom_B_bin3),(num_S/denom_S_bin3) )
    for i in range(1,6):
        num_S = float( S_bin3.Integral(407-i,602) )
        num_B = float( B_bin3.Integral(407-i,602) )
        g3.SetPoint(i+43,(num_S/denom_S_bin3),1-(num_B/denom_B_bin3))
        # g_new.SetPoint(i+43,(num_B/denom_B_bin3),(num_S/denom_S_bin3) )

    

    

    g_subjet = TGraph(49)
    for i in range(5):
        num_S_subjet = float( h2_S_subjet.Integral(602-i,602) )
        num_B_subjet = float( h2_B_subjet.Integral(602-i,602) )
        g_subjet.SetPoint( i,(num_S_subjet/denom_S_all),1-(num_B_subjet/denom_B_all) )
        # g_subjet.SetPoint( i,(num_B_subjet/denom_B_all),(num_S_subjet/denom_S_all) )

    for i in range(1,40):
        num_S_subjet = float( h2_S_subjet.Integral(602-(i*5),602) )
        num_B_subjet = float( h2_B_subjet.Integral(602-(i*5),602) )
        g_subjet.SetPoint( i+4,(num_S_subjet/denom_S_all),1-(num_B_subjet/denom_B_all) )
        # g_subjet.SetPoint(i+4,(num_B_subjet/denom_B_all),(num_S_subjet/denom_S_all) )
    for i in range(1,6):
        num_S_subjet = float( h2_S_subjet.Integral(407-i,602) )
        num_B_subjet = float( h2_B_subjet.Integral(407-i,602) )
        g_subjet.SetPoint(i+43,(num_S_subjet/denom_S_all),1-(num_B_subjet/denom_B_all))
        # g_subjet.SetPoint(i+43,(num_B_subjet/denom_B_all),(num_S_subjet/denom_S_all) )
        
    # denom_S_1 = float( S_bin1_subjet.Integral(380,610) )
 #    denom_B_1 = float( B_bin1_subjet.Integral(380,610) )
 #    g1_subjet = TGraph(49)
 #
 #    for i in range(5):
 #        num_S = float( S_bin1_subjet.Integral(602-i,602) )
 #        num_B = float( B_bin1_subjet.Integral(602-i,602) )
 #        g1_subjet.SetPoint( i,(num_S/denom_S_1),1-(num_B/denom_B_1) )
 #        # g1.SetPoint( i,(num_B/denom_B_1),(num_S/denom_S_1) )
 #
 #    for i in range(1,40):
 #        num_S = float( S_bin1_subjet.Integral(602-(i*5),602) )
 #        num_B = float( B_bin1_subjet.Integral(602-(i*5),602) )
 #        g1_subjet.SetPoint( i+4,(num_S/denom_S_1),1-(num_B/denom_B_1) )
 #        # g1.SetPoint(i+4,(num_B/denom_B_1),(num_S/denom_S_1) )
 #    for i in range(1,6):
 #        num_S = float( S_bin1_subjet.Integral(407-i,602) )
 #        num_B = float( B_bin1_subjet.Integral(407-i,602) )
 #        g1_subjet.SetPoint(i+43,(num_S/denom_S_1),1-(num_B/denom_B_1))
 #        # g_new.SetPoint(i+43,(num_B/denom_B_1),(num_S/denom_S_1) )
   
       #
    # denom_S_1 = float( S_bin1_baseline.Integral(380,610) )
    # denom_B_1 = float( B_bin1_baseline.Integral(380,610) )
    # g1_baseline = TGraph(49)
    #
    # for i in range(5):
    #     num_S = float( S_bin1_baseline.Integral(602-i,602) )
    #     num_B = float( B_bin1_baseline.Integral(602-i,602) )
    #     g1_baseline.SetPoint( i,(num_S/denom_S_1),1-(num_B/denom_B_1) )
    #     # g1.SetPoint( i,(num_B/denom_B_1),(num_S/denom_S_1) )
    #
    # for i in range(1,40):
    #     num_S = float( S_bin1_baseline.Integral(602-(i*5),602) )
    #     num_B = float( B_bin1_baseline.Integral(602-(i*5),602) )
    #     g1_baseline.SetPoint( i+4,(num_S/denom_S_1),1-(num_B/denom_B_1) )
    #     # g1.SetPoint(i+4,(num_B/denom_B_1),(num_S/denom_S_1) )
    # for i in range(1,6):
    #     num_S = float( S_bin1_baseline.Integral(407-i,602) )
    #     num_B = float( B_bin1_baseline.Integral(407-i,602) )
    #     g1_baseline.SetPoint(i+43,(num_S/denom_S_1),1-(num_B/denom_B_1))
    #
    # denom_S_1 = float( S_bin2_subjet.Integral(380,610) )
 #    denom_B_1 = float( B_bin2_subjet.Integral(380,610) )
 #    g2_subjet = TGraph(49)
 #
 #    for i in range(5):
 #        num_S = float( S_bin2_subjet.Integral(602-i,602) )
 #        num_B = float( B_bin2_subjet.Integral(602-i,602) )
 #        g2_subjet.SetPoint( i,(num_S/denom_S_1),1-(num_B/denom_B_1) )
 #        # g1.SetPoint( i,(num_B/denom_B_1),(num_S/denom_S_1) )
 #
 #    for i in range(1,40):
 #        num_S = float( S_bin2_subjet.Integral(602-(i*5),602) )
 #        num_B = float( B_bin2_subjet.Integral(602-(i*5),602) )
 #        g2_subjet.SetPoint( i+4,(num_S/denom_S_1),1-(num_B/denom_B_1) )
 #        # g1.SetPoint(i+4,(num_B/denom_B_1),(num_S/denom_S_1) )
 #    for i in range(1,6):
 #        num_S = float( S_bin2_subjet.Integral(407-i,602) )
 #        num_B = float( B_bin2_subjet.Integral(407-i,602) )
 #        g2_subjet.SetPoint(i+43,(num_S/denom_S_1),1-(num_B/denom_B_1))
 #        # g_new.SetPoint(i+43,(num_B/denom_B_1),(num_S/denom_S_1) )
 #
 #
 #    denom_S_1 = float( S_bin3_subjet.Integral(380,610) )
 #    denom_B_1 = float( B_bin3_subjet.Integral(380,610) )
 #
 #    g3_subjet = TGraph(49)
 #
 #    for i in range(5):
 #        num_S = float( S_bin3_subjet.Integral(602-i,602) )
 #        num_B = float( B_bin3_subjet.Integral(602-i,602) )
 #        g3_subjet.SetPoint( i,(num_S/denom_S_1),1-(num_B/denom_B_1) )
 #        # g3.SetPoint( i,(num_B/denom_B_1),(num_S/denom_S_1) )
 #
 #    for i in range(1,40):
 #        num_S = float( S_bin3_subjet.Integral(602-(i*5),602) )
 #        num_B = float( B_bin3_subjet.Integral(602-(i*5),602) )
 #        g3_subjet.SetPoint( i+4,(num_S/denom_S_1),1-(num_B/denom_B_1) )
 #        # g3.SetPoint(i+4,(num_B/denom_B_1),(num_S/denom_S_1) )
 #    for i in range(1,6):
 #        num_S = float( S_bin3_subjet.Integral(407-i,602) )
 #        num_B = float( B_bin3_subjet.Integral(407-i,602) )
 #        g3_subjet.SetPoint(i+43,(num_S/denom_S_1),1-(num_B/denom_B_1))
 #        # g_new.SetPoint(i+43,(num_B/denom_B_1),(num_S/denom_S_1) )
        
       
    mg.append(g_new)     
    mg.append(g1)
    mg.append(g2)
    mg.append(g3)
    # mg.append(g_baseline)
 #    mg.append(g1_baseline)
    mg.append(g_subjet) 
    # mg.append(g1_subjet)
    # mg.append(g2_subjet)
    # mg.append(g3_subjet)

    return mg

def formatGraph(graph, graphNum):
    colors = [ kGreen+2, kRed, kBlue, kBlack, kMagenta, kOrange+2, kCyan ]
    graphColor = colors[graphNum % 7]
    lineStyle = (graphNum % 11) + 1
    graph.SetLineColor(graphColor)
    graph.SetLineStyle(lineStyle)
    graph.SetLineWidth(2)

def plotPerformanceCurves(graphs, ordering, fTitle, fXAxisTitle, fYAxisTitle, fExtraInfo, fOutputFile, fXmin, fXmax, fYmin, fYmax, fLogy=0):

    # gROOT.SetBatch(kTRUE)
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

    legend = TLegend(.16,.54,.36,.73)
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
        graph.Draw("L")
        graphCounter += 1

    if (fLogy):
        c.SetLogy()
    legend.Draw()
    l1 = TLatex()
    l1.SetTextAlign(13)
    l1.SetTextFont(42)
    l1.SetNDC()
    l1.SetTextSize(0.04)
    l1.DrawLatex(0.14+0.03,0.25, fTitle)

    l1.SetTextAlign(12)
    l1.SetTextSize(0.045)
    l1.SetTextFont(62)
    l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")
    
    l1.SetTextAlign(12)
    l1.SetTextSize(0.035)
    l1.SetTextFont(61)
    l1.DrawLatex(0.13,0.96, "CMS")
    l1.SetTextSize(0.03)
    l1.SetTextFont(52)
    l1.DrawLatex(0.21,0.96, "Preliminary")

    l1.SetTextFont(42)
    l1.SetTextSize(0.025)
    l1.DrawLatex(0.2,0.45, "AK 0.8")
    l1.DrawLatex(0.2,0.42, fExtraInfo)

    c.SaveAs(fOutputFile)
    f = TFile("file3.root","UPDATE");
    c.Write()


def makePlots():


   ordering = [] # vectors storing the order of legend entries
   mg = [] # maps to hold legend entries and TGraph*s

   mg = getPerformanceCurve("validation/tau21_validation_rAll_forTraining.root","validation/tau21_validation_qcd_forTraining.root",300.,2000.)
   
   # ordering.append("Inclusive QCD")
   # ordering.append("Baseline")
   # ordering.append("Subjet CSV")
   ordering.append("Double-b tag: All")
   ordering.append("Double-b tag: 300 GeV < p_{T} < 470 GeV")
   ordering.append("Double-b tag: 470 GeV < p_{T} < 600 GeV")
   ordering.append("Double-b tag: p_{T} > 600 GeV")
   ordering.append("Subjet CSV: All")
   # ordering.append("Subjet CSV: 300 GeV < p_{T} < 470 GeV")
   # ordering.append("Subjet CSV: 470 GeV < p_{T} < 600 GeV")
   # ordering.append("Subjet CSV: p_{T} > 600 GeV")
   # ordering.append("Inclusive: All")
   # ordering.append("Inclusive: #tau_{21} < 0.4")
   # ordering.append("Baseline: All")
   # ordering.append("Baseline: #tau_{21} < 0.4")
   # ordering.append("Subjet CSV: All")
   # ordering.append("Subjet CSV: #tau_{21} < 0.4")
   
   


   plotPerformanceCurves(mg,ordering,"","Tagging efficiency (H#rightarrowb#bar{b})","1 - mistagging efficiency (GSP)","70 GeV < M_{p} < 200 GeV , p_{T} > 300 GeV","CLEANED_GSP.png",0, 1, 1E-3, 1, 0)
   
   


if __name__ == "__main__":
    makePlots()