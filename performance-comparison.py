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
# gStyle.SetStatH(0.3);   # Max height of stats box
# gStyle.SetStatW(0.25);  # Max height of stats box
gStyle.SetPadLeftMargin(0.20)   # Left margin of the pads on the canvas.
gStyle.SetPadBottomMargin(0.20) # Bottom margin of the pads on the canvas.
# gStyle.SetFrameFillStyle(0) # Keep the fill color of our pads white.

f = ROOT.TFile.Open('TMVA_classification.root', 'READ') 
bdtcat=f.Get('Method_Category/BDTCat/MVA_BDTCat_rejBvsS') 
bdtg=f.Get('Method_BDT/BDTG/MVA_BDTG_rejBvsS') 

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
  for j in range(0,2):
    hname = "histos%d_%d" % (i, j) # Each histogram must have a unique name
    htitle = "Histogram %d %d" % (i, j) # Give each its own title.
    if (j == 0):
      histos[i].append(bdtg)
    elif (j == 1):
      histos[i].append(bdtcat)
    # histos[i][j].SetMinimum(0)
    histos[i][j].SetLineColor(j+2)
    histos[i][j].SetLineWidth(2)
    histos[i][j].GetXaxis().SetNdivisions(10)
    histos[i][j].GetXaxis().SetLabelSize(0.06)
    # histos[i][j].GetXaxis().CenterTitle()
    histos[i][j].GetXaxis().SetTitleSize(0.06)
    histos[i][j].GetXaxis().SetTitleOffset(0.8)
    histos[i][j].GetXaxis().SetTitle( "Signal efficiency" )

    histos[i][j].GetYaxis().SetNdivisions(10)
    histos[i][j].GetYaxis().SetLabelSize(0.06)
    # histos[i][j].GetYaxis().CenterTitle()
    histos[i][j].GetYaxis().SetTitleSize(0.06)
    histos[i][j].GetYaxis().SetTitleOffset(.8)
    histos[i][j].GetYaxis().SetTitle("1-bkg. efficiency")
    l.AddEntry(histos[i][j],histos[i][j].GetTitle(),'f')
    

num_canvases = 1
can = []
for i in range(0, num_canvases):
  name = "can%d" % (i) 
  title = "pT %d" % (i) 
  can.append(TCanvas( name, title, 10+10*i, 10+10*i, 800, 800 ))
  can[i].SetFillColor( 0 )
  can[i].Divide(0 , 2 )


can[0].cd(1) 
gPad.SetGridx()
gPad.SetGridy()        
histos[0][0].Draw("HIST")   
histos[0][1].Draw("HISTsame")
l.Draw()
gPad.Update()
# can[0].cd(2)
#     histos[0][2].Draw("HIST")
#     histos[0][3].Draw("HISTsame")
#     l.Draw()
#     gPad.Update()

time.sleep(100)
f.Close()