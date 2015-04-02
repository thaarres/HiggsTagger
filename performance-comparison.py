from optparse import OptionParser
from ROOT import *
import ROOT
import sys
import time
import gc
import math
import array

gROOT.Reset()
gStyle.SetOptStat(0)  # What is displayed in the stats box for each histo.
gStyle.SetOptTitle(0)
# gStyle.SetStatH(0.3);   # Max height of stats box
# gStyle.SetStatW(0.25);  # Max height of stats box
gStyle.SetPadLeftMargin(0.20)   # Left margin of the pads on the canvas.
gStyle.SetPadBottomMargin(0.20) # Bottom margin of the pads on the canvas.
# gStyle.SetFrameFillStyle(0) # Keep the fill color of our pads white.

fRew = ROOT.TFile.Open('TMVA_reweighted.root', 'READ') 
fUnw = ROOT.TFile.Open('TMVA_unweighted_wPt.root', 'READ')

bdtcat4=fRew.Get('Method_Category/BDTCat4/MVA_BDTCat4_rejBvsS') 
bdtcat12=fRew.Get('Method_Category/BDTCat12/MVA_BDTCat12_rejBvsS') 
bdtg=fRew.Get('Method_BDT/BDTG/MVA_BDTG_rejBvsS') 
# bdtg_flatptEta=f2.Get('Method_BDT/BDTG/MVA_BDTG_rejBvsS')
bdtg_flatptEta=fUnw.Get('Method_Category/BDTCat12/MVA_BDTCat12_rejBvsS') 
l = ROOT.TLegend(0.21,0.2,0.39,0.36,"","NDC")
l.SetLineWidth(2)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetTextFont(42)
l.SetTextSize(0.04)
l.SetTextAlign(12)

histos = []
for i in range(0,1):
  histos.append([])
  for j in range(0,4):
    hname = "histos%d_%d" % (i, j) # Each histogram must have a unique name
    htitle = "Histogram %d %d" % (i, j) # Give each its own title.
    if (j == 0):
      histos[i].append(bdtg)
    elif (j == 1):
      histos[i].append(bdtcat4)
    elif (j == 2):
      histos[i].append(bdtcat12)  
      histos[i][j].SetTitle("p_{T}-#eta rew." )
    elif (j == 3):
      histos[i].append(bdtg_flatptEta)
      # histos[i][j].SetTitle("p_{T}-#eta rew." )
      histos[i][j].SetTitle("Unweighted (w/p_{T})" )
      
    histos[i][j].SetMinimum(0)
    histos[i][j].SetLineColor(j+2)
    histos[i][j].SetLineWidth(2)
    histos[i][j].GetXaxis().SetNdivisions(10)
    histos[i][j].GetXaxis().SetLabelSize(0.06)
    # histos[i][j].GetXaxis().CenterTitle()
    histos[i][j].GetXaxis().SetTitleSize(0.05)
    histos[i][j].GetXaxis().SetTitleOffset(1.5)
    histos[i][j].GetXaxis().SetTitle( "Signal efficiency" )

    histos[i][j].GetYaxis().SetNdivisions(10)
    histos[i][j].GetYaxis().SetLabelSize(0.06)
    # histos[i][j].GetYaxis().CenterTitle()
    histos[i][j].GetYaxis().SetTitleSize(0.05)
    histos[i][j].GetYaxis().SetTitleOffset(1.5)
    histos[i][j].GetYaxis().SetTitle("1-bkg. efficiency")
    # l.AddEntry(histos[i][j],histos[i][j].GetTitle(),'f')
    bin = histos[i][j].FindLastBinAbove(0.90,1)
    
    
l.AddEntry(histos[0][2],histos[0][2].GetTitle(),'f')
l.AddEntry(histos[0][3],histos[0][3].GetTitle(),'f')
num_canvases = 1
can = []
for i in range(0, num_canvases):
  name = "can%d" % (i) 
  title = "pT %d" % (i) 
  can.append(TCanvas( name, title, 10+10*i, 10+10*i, 900, 800 ))
  can[i].SetFillColor( 0 )
  # can[i].Divide(0 , 2 )


can[0].cd(1)
 
gPad.SetGridx()
gPad.SetGridy()        
# histos[0][0].Draw("HIST")
# histos[0][1].Draw("HISTsame")
histos[0][2].Draw("HIST")
histos[0][3].Draw("HISTsame")
l.Draw()
gPad.Update()
# can[0].cd(2)
#     histos[0][2].Draw("HIST")
#     histos[0][3].Draw("HISTsame")
#     l.Draw()
#     gPad.Update()

rew_bdtcat4=fRew.Get('Method_Category/BDTCat4/MVA_BDTCat4_effB') 
rew_bdtcat4.SetTitle("rew cat4")
rew_bdtcat12=fRew.Get('Method_Category/BDTCat12/MVA_BDTCat12_effB') 
rew_bdtcat12.SetTitle("rew cat12")
rew_bdtg=fRew.Get('Method_BDT/BDTG/MVA_BDTG_effB')
rew_bdtg.SetTitle("rew bdtg")

unw_bdtcat4=fUnw.Get('Method_Category/BDTCat4/MVA_BDTCat4_effB') 
unw_bdtcat4.SetTitle("unw cat4")
unw_bdtcat12=fUnw.Get('Method_Category/BDTCat12/MVA_BDTCat12_effB')
unw_bdtcat12.SetTitle("unw cat12" )
unw_bdtg=fUnw.Get('Method_BDT/BDTG/MVA_BDTG_effB') 
unw_bdtg.SetTitle("unw bdtg")

histos2 = []
for j in range(0,6):
  hname = "histos2_%d" % (j)
  htitle = "Histogram2 %d" % (j) # Give each its own title.
  if (j == 0):
    histos2.append(rew_bdtcat4)   
  elif (j == 1):
    histos2.append(rew_bdtcat12)
  elif (j == 2):
    histos2.append(rew_bdtg)
  elif (j == 3):
    histos2.append(unw_bdtcat4)
  elif (j == 4):
    histos2.append(unw_bdtcat12)
  elif (j == 5):
    histos2.append(unw_bdtg)

mistag = 0.10
for h in histos2:
  bin = h.FindLastBinAbove(mistag,1)
  print "For %s :" %(h.GetTitle())
  print "Purity = %2f" %(1-h.GetBinContent(bin))
  print "Cut value = %3f" %h.GetBinCenter(bin)
  print "################################"
  # pT_weight = pT_reweight_2b->GetBinContent( bin );
time.sleep(100)
f.Close()