import ROOT 
import sys

if len(sys.argv) !=4: 
  print("USAGE: %s <input file data> <input file mc> <output file>" % (sys.argv[0])) 

  sys.exit(1)

inFileName_data = sys.argv[1] 
inFileName_mc = sys.argv[2] 
outFileName = sys.argv[3] 

print("Reading from", inFileName_data, "and writing to", outFileName)
print("Reading from", inFileName_mc, "and writing to", outFileName) 

inFile_data = ROOT.TFile.Open(inFileName_data, "READ") 
inFile_mc = ROOT.TFile.Open(inFileName_mc, "READ")  

tree = inFile_data.Get("HASCO") 
  

mll_data = ROOT.TH1D("data","m_{ll}, data",150,50.e3,200.e3) 



mmll = [] 
mll_data.Sumw2() 
for entryNum in range (0,tree.GetEntries()):
  tree.GetEntry(entryNum)
  if getattr(tree, "lep_n") != 2: 
    continue
  lepton0 = ROOT.TLorentzVector()
  lepton1 = ROOT.TLorentzVector()

  pt = getattr(tree,"lep_pt")
  eta = getattr(tree,"lep_eta")
  phi = getattr(tree,"lep_phi") 
  nrg = getattr(tree,"lep_E") 

  lepton0.SetPtEtaPhiE(pt[0],eta[0],phi[0],nrg[0]) 
  lepton1.SetPtEtaPhiE(pt[1],eta[1],phi[1],nrg[1])

  dilepton = lepton0 + lepton1
  dileptonMass = dilepton.M() 


  mll_data.Fill(dileptonMass) 
mll_data.SetDirectory(0)  

tree = inFile_mc.Get("HASCO") 

mll_mc= ROOT.TH1F("mc", "m_{ll}, mc", 150, 50.e3,200.e3) 

mll_mc.Sumw2()  
for entryNum in range (0,tree.GetEntries()):
  tree.GetEntry(entryNum)
  if getattr(tree, "lep_n") != 2:
    continue
  lepton0 = ROOT.TLorentzVector()
  lepton1 = ROOT.TLorentzVector()

  pt = getattr(tree,"lep_pt")
  eta = getattr(tree,"lep_eta")
  phi = getattr(tree,"lep_phi")
  nrg = getattr(tree,"lep_E") 

  lepton0.SetPtEtaPhiE(pt[0],eta[0],phi[0],nrg[0]) 
  lepton1.SetPtEtaPhiE(pt[1],eta[1],phi[1],nrg[1])

  dilepton = lepton0 + lepton1
  dileptonMass = dilepton.M() 


  weight = 1.0

  weight*= getattr(tree,"mcWeight")
  weight*= getattr(tree,"scaleFactor_PILEUP") 
  weight*= getattr(tree,"scaleFactor_MUON")
  weight*= getattr(tree,"scaleFactor_TRIGGER") 
  mll_mc.Fill(dileptonMass, weight)

  
mll_mc.SetDirectory(0)

inFile_data.Close()
inFile_mc.Close()

outHistFile = ROOT.TFile.Open(outFileName ,"RECREATE")
outHistFile.cd() 

mll_data.Write() 
mll_mc.Write()



outHistFile.Close()



