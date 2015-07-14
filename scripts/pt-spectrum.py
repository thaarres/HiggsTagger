from ROOT import *
import math

file_S1 = TFile("new/rAll_forTraining.root")
file_S2 = TFile("new/ttbar_forTraining.root")
file_B1 = TFile("new/qcd_forTraining.root")
     
    
h2_S_1 = TH1F("hBDTGDisc_S1","",100,300.,1500.)
h2_S_2 = TH1F("hBDTGDisc_S2","",100,300.,1500.)
h2_B_1 = TH1F("hBDTGDisc_B1","",100,300.,1500.)
h2_B_2 = TH1F("hBDTGDisc_B2","",100,300.,1500.)    
    
treeS1=file_S1.Get('Fjets') 
treeS2=file_S2.Get('Fjets') 
treeB=file_B1.Get('Fjets') 

S1entry = treeS1.GetEntries() 
S2entry = treeS2.GetEntries() 
Bentry = treeB.GetEntries() 

for event in treeS1:
  # if (abs(event.flavour)==5):
    h2_S_1.Fill( event.ptGroomed )
        
for event in treeS2:
  if (abs(event.flavour)==5 and event.nbHadrons<2):
    h2_S_2.Fill( event.ptGroomed )
        
for event in treeB:
  if (abs(event.flavour)==5 and event.nbHadrons<2):
    h2_B_1.Fill( event.ptGroomed )
  if (abs(event.flavour)==5 and event.nbHadrons>1):
    h2_B_2.Fill( event.ptGroomed )      

h2_S_1.Scale( 1./h2_S_1.Integral() )
h2_S_2.Scale( 1./h2_S_2.Integral() )
h2_B_1.Scale( 1./h2_B_1.Integral() )
h2_B_2.Scale( 1./h2_B_2.Integral() )

h2_S_1.SetLineColor(kGreen+2)
h2_S_1.SetLineStyle(1)
h2_S_1.SetLineWidth(2)

h2_S_2.SetLineColor(kRed)
h2_S_2.SetLineStyle(2)
h2_S_2.SetLineWidth(2)

h2_B_1.SetLineColor(kBlue)
h2_B_1.SetLineStyle(4)
h2_B_1.SetLineWidth(2)

h2_B_2.SetLineColor(kAzure+7)
h2_B_2.SetLineStyle(3)
h2_B_2.SetLineWidth(2)

gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()

c = TCanvas("c", "",800,800)
c.cd()
# h2_S_1.GetXaxis().SetTitle("p_{T}")
h2_S_2.GetXaxis().SetTitle("p_{T} [GeV]")
h2_S_2.GetYaxis().SetTitle("A.U")
h2_S_2.SetTitleOffset(1.2,"X")
h2_S_2.SetTitleOffset(1.7,"Y")
h2_S_2.Draw("hist")
h2_S_1.Draw("histSAME")
h2_B_1.Draw("histSAME")
h2_B_2.Draw("histSAME")
c.SetGridx()
c.SetGridy()

legend = TLegend(.76,.64,.89,.77)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.021)
legend.AddEntry(h2_S_1,"R (0.6-2.0 TeV)","l")
legend.AddEntry(h2_S_2,"b t#bar{t}","l")
legend.AddEntry(h2_B_1,"b QCD","l")
legend.AddEntry(h2_B_2,"bb QCD","l")
legend.Draw()

l1 = TLatex()
l1.SetTextAlign(13)
l1.SetTextFont(42)
l1.SetNDC()
l1.SetTextSize(0.04)
l1.DrawLatex(0.14+0.03,0.85, "")

l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)
l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

l1.SetTextSize(0.035)
l1.SetTextFont(61)
l1.DrawLatex(0.13,0.96, "CMS")
l1.SetTextSize(0.03)
l1.SetTextFont(52)
l1.DrawLatex(0.21,0.96, "Preliminary")

l1.SetTextFont(42)
l1.SetTextSize(0.025)
l1.DrawLatex(0.52,0.45, "AK 0.8")
l1.DrawLatex(0.52,0.42, "70 GeV < M_{p} < 200 GeV , p_{T} > 300 GeV")

c.SaveAs("validationplots/pT-spectrum_AK08.pdf")

