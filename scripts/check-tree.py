from ROOT import *
import time
import sys
import os, commands

files = []

inDirName = '/shome/thaarres/HiggsTagger/Spring15/rootfiles/qcd/scaled'

for inFileName in os.listdir(inDirName):
  if inFileName.endswith(".root"):
    name = inDirName + '/' + inFileName
    filetmp = TFile.Open(name,'READ')
    files.append(filetmp)
    print 'Appending file %s to filelist' %inFileName

gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()

histos = []

for j in range(0,3):
  hname = "histos_%d" % (j) # Each histogram must have a unique name
  htitle = ""  
  histos.append( TH1F(hname, htitle, 800, 0., 2000.) )  
  histos[j].GetXaxis().SetTitle( "p_{T}" )
  histos[j].GetYaxis().SetTitle( "Events" )
  histos[j].SetLineColor(j-12)
  histos[j].SetLineStyle(2)
  histos[j].SetLineWidth(2)
          
    
for f in files:
  mytree=f.Get('Fjets') 
  nentry = mytree.GetEntries()
  weight = mytree.GetWeight()
  print 'Using event weight %f' %weight
  for event in mytree:
    histos[0].Fill( event.ptPruned, weight )
       
c3 = TCanvas("c3", "",800,800)
c3.cd()
histos[0].Draw("HIST")


time.sleep(200)
f.Close()