import ROOT # Script for Invariant mass of First Four Jets
import sys

file_path = "/Users/isaacanokye/Desktop/USATLAS24/game.root"
root_file = ROOT.TFile.Open(file_path)

if not root_file or root_file.IsZombie():
    print("Error: Failed to open ROOT file.")
    sys.exit(1)

tree = root_file.Get("ntuple") 
if not tree:
    print("Error: Tree not found in the file.")
    sys.exit(1)

hist_jet_pt = ROOT.TH1F("hist_jet_pt", "Transverse Momentum of Jets; p_{T} [GeV]; Events", 100, 0, 2000)
hist_jet_eta = ROOT.TH1F("hist_jet_eta", "Pseudorapidity of Jets; eta; Events", 100, 0, 10)
hist_jet_phi = ROOT.TH1F("hist_jet_phi", "Azimuthal Angle of Jets; phi; Events", 100, 0,1000)
hist_jet_m = ROOT.TH1F("hist_jet_m", "Mass of Jets; m [GeV]; Events", 100, 0, 200)
hist_jetMass = ROOT.TH1F("hist_jetMass", "Invariant mass of First Four Jets; Mass [GeV]; Events", 100, 0, 1000000)

nEntries = tree.GetEntries()
for entryNum in range(nEntries):
    tree.GetEntry(entryNum)
    jet_pt = getattr(tree, "AntiKt4emtopoCalo422Jets_pt")
    jet_eta = getattr(tree, "AntiKt4emtopoCalo422Jets_eta")
    jet_phi = getattr(tree, "AntiKt4emtopoCalo422Jets_phi")
    jet_m = getattr(tree, "AntiKt4emtopoCalo422Jets_m") 

    if len(jet_pt) >= 4: 
        jet_system = ROOT.TLorentzVector()
        for j in range(4):  
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM(jet_pt[j], jet_eta[j], jet_phi[j], jet_m[j])
            jet_system += jet  

        hist_jetMass.Fill(jet_system.M()) 

        for j in range(len(jet_pt)):  
            hist_jet_pt.Fill(jet_pt[j])
            hist_jet_eta.Fill(jet_eta[j])
            hist_jet_phi.Fill(jet_phi[j])
            hist_jet_m.Fill(jet_m[j])

print("Number of entries in the tree:", nEntries)

canvas_jetMass = ROOT.TCanvas("canvas_jetMass", "Jet Mass System")
hist_jetMass.Draw()
canvas_jetMass.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/plots_jetMassVar.pdf") 


 
