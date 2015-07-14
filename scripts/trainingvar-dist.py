from ROOT import *
import time
import array

files = []
vars = [
  # "PFLepton_ptrel",
  # "z_ratio",
  # "tau_dot",
 # "SV_mass_0"
  "SV_vtx_EnergyRatio_0",
  "SV_vtx_EnergyRatio_1",
  # "PFLepton_IP2D"
  # "tau2/tau1"
   # "nSV",
   # "nSL",
   #
  ]
varDict = {}
for var in vars:
  varDict[var] = array.array('f',[0]) 
  
files.append('new/rAll_forTraining.root')
files.append('new/qcd_forTraining.root')
files.append('new/ttbar_forTraining.root')

gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()

histos = []

for j in range(0,len(vars)*4):
  hname = "histos_%d" % (j)
  htitle = ""
  # if (vars[j].find("z_ratio") != -1 or vars[j].find("tau2/tau1") != -1):
    # histos.append( TH1F(hname,"",200, 0., 1.) )
  # elif (vars[j].find("PFLepton_ptrel") != -1):
  # histos.append( TH1F(hname,"",200, 0., 25.) )
  # # elif (vars[j].find("tau_dot") != -1):
  #   histos.append( TH1F(hname,"",200, -1., 1.) )
  # # elif (vars[j].find("SV_mass_0") != -1):
  # histos.append( TH1F(hname,"",200, -1., 7.) )
  # # elif (vars[j].find("SV_vtx_EnergyRatio") != -1):
  histos.append( TH1F(hname,"",200, -1., 15.) )
  # # elif (vars[j].find("PFLepton_IP2D") != -1):
  # histos.append( TH1F(hname,"",100, -40., 40.) )
  # # else:
  # histos.append( TH1F(hname,"",13, 0., 12.) )
      
  if (j < len(vars) ):
    histos[j].GetXaxis().SetTitle( vars[j] )
    histos[j].SetLineColor(kBlack)
    
  elif (j >= len(vars) and j < 2*len(vars)):
    histos[j].SetLineColor(kGreen)
    histos[j].SetLineStyle(3)
  elif (j >= 2*len(vars) and j < 3*len(vars)):
    histos[j].SetLineColor(kAzure+0)
    histos[j].SetLineStyle(4)
  elif (j >=3*len(vars) and j < 4*len(vars)):
    histos[j].SetLineColor(kRed+1)
    histos[j].SetLineStyle(5)
  # elif (4*len(vars) <= j < 5*len(vars)):
 #    histos[j].SetLineColor(kYellow)
 #    histos[j].SetLineStyle(6)
 #  elif (5*len(vars) <= j < 6*len(vars)):
 #    histos[j].SetLineColor(kViolet+1)
 #    histos[j].SetLineStyle(2)
  histos[j].GetYaxis().SetTitle( "A.U" ) 
  histos[j].GetYaxis().SetTitleOffset( 1.8 ) 
  histos[j].SetLineWidth(2)
  # histos[j].SetBit(TH1.kCanRebin)
          
    
for t in files:
  f = TFile(t,"read")
  mytree=f.Get('Fjets')
  nentry = mytree.GetEntries()

  for event in mytree:
    
    if(f.GetName().find("rAll") != -1):
        i = -1
        for var in vars:
          i += 1
          if var.find("tau2/tau1") != -1:
            varDict[var][0] = getattr(mytree, "tau2")
            varDict[var][0] /= getattr(mytree, "tau1")
          else:
            varDict[var][0] = getattr(mytree, var)
          histos[i].Fill(varDict[var][0])
          
    elif(f.GetName().find("qcd") != -1):
      if(abs(event.flavour)==5):
        i = -1
        for var in vars:
          i += 1
          if var.find("tau2/tau1") != -1:
            varDict[var][0] = getattr(mytree, "tau2")
            varDict[var][0] /= getattr(mytree, "tau1")
          else:
            varDict[var][0] = getattr(mytree, var)
          if(event.nbHadrons<2):
            histos[i+len(vars)].Fill(varDict[var][0])
          if(event.nbHadrons>1):
            histos[i+2*len(vars)].Fill(varDict[var][0])
            
    elif(f.GetName().find("ttbar") != -1):
      if(abs(event.flavour)==5 and event.nbHadrons<2):
        i = -1
        for var in vars:
          i += 1
          if var.find("tau2/tau1") != -1:
            varDict[var][0] = getattr(mytree, "tau2")
            varDict[var][0] /= getattr(mytree, "tau1")
          else:
            varDict[var][0] = getattr(mytree, var)
          # if( abs(event.SubJet1_flavour)==4 or abs(event.SubJet2_flavour)==4 ):
#             histos[i+4*len(vars)].Fill(varDict[var][0])
#           if( abs(event.SubJet1_flavour)<4 or abs(event.SubJet2_flavour)<4 ):
#             histos[i+5*len(vars)].Fill(varDict[var][0])
#           else:
          histos[i+3*len(vars)].Fill(varDict[var][0])
         

for j in range(0,len(histos)):
  # histos[j].Rebin(10)
  histos[j].Scale(1./(histos[j].Integral()))

c = []
for j in range(0,len(vars)):
  print "Drawing histogram for variable %s" %(vars[j])
  c.append(TCanvas("c_%d" %j, "",800,800))
  
legend2 = TLegend(.64,.6,.85,.85)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.04)
legend2.AddEntry(histos[0],"R(0.6-2.0 TeV)",'l')
legend2.AddEntry(histos[0+len(vars)],"QCD b ",'l')
legend2.AddEntry(histos[0+2*len(vars)],"QCD bb",'l')
legend2.AddEntry(histos[0+3*len(vars)],"t#bar{t} b",'l')
# legend2.AddEntry(histos[0+4*len(vars)],"t#bar{t} b-c",'l')
# legend2.AddEntry(histos[0+5*len(vars)],"t#bar{t} b-light",'l')



l1 = TLatex()
l1.SetNDC()
  
for j in range(0,len(vars)):
  c[j].cd()
  if (vars[j].find("SV_mass_0") != -1 or vars[j].find("SV_vtx_EnergyRatio") != -1 or vars[j].find("tau_dot") != -1 or vars[j].find("PFLepton_IP2D") != -1):
    c[j].SetLogy()
  histos[j].SetMaximum(4.0*histos[j].GetMaximum())
  # histos[j].GetXaxis().SetRange(histos[j+3*len(vars)].FindFirstBinAbove(0.,1),histos[j+3*len(vars)].FindLastBinAbove(0.,1))
  # histos[j].SetBins(histos[j].GetNbinsX(), histos[j].GetXaxis().GetXmin(),histos[j].GetXaxis().GetXmax() )
  histos[j].Draw("HIST")
  histos[j+1*len(vars)].Draw("HISTsame")
  histos[j+2*len(vars)].Draw("HISTsame")
  histos[j+3*len(vars)].Draw("HISTsame")
  # histos[j+4*len(vars)].Draw("HISTsame")
  # histos[j+5*len(vars)].Draw("HISTsame")

  
  legend2.Draw("same")
  
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
  l1.DrawLatex(0.2,0.90, "AK 0.8")
  l1.DrawLatex(0.2,0.86, "70 GeV < M_{p} < 200 GeV , p_{T} > 300 GeV")
  
  c[j].SetGridx()
  c[j].SetGridy()
  c[j].Update()
  c[j].SaveAs("/shome/thaarres/Notes/notes/AN-15-073/trunk/Figures/performance/variable-plots/"+histos[j].GetXaxis().GetTitle()+".pdf")


time.sleep(200)
f.Close()