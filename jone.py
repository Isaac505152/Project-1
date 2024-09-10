import ROOT  #Script for 1st jet
import sys


file_path = "/Users/isaacanokye/Desktop/USATLAS24/bay.root" 

root_file = ROOT.TFile.Open(file_path)

if not root_file or root_file.IsZombie():
    print("Error: Failed to open ROOT file.")
    sys.exit(1)

tree = root_file.Get("ntuple")
if not tree:
    print("Error: Tree not found in the file.")
    sys.exit(1)

hist_jet_pt = ROOT.TH1F("hist_jet_pt", "Pt of Most Energetic Jet; p_{T} [GeV]; Events", 100, 0, 200000)
hist_jet_eta = ROOT.TH1F("hist_jet_eta", "Pseudorapidity of Jets; eta; Events", 10, 0, 10)
hist_jet_phi = ROOT.TH1F("hist_jet_phi", "Azimuthal Angle of Jets; phi; Events", 100, 0, 200000)
hist_jet_m = ROOT.TH1F("hist_jet_m", "Mass of Jets; m [GeV]; Events", 100, 0, 200000)
#hist_jetMass = ROOT.TH1F("hist_jetMass", "Pt of the Most Energetic Jet; Mass [MeV]; Events", 100, 0, 100000) 


nEntries = tree.GetEntries()

for entryNum in range(nEntries):
    tree.GetEntry(entryNum)
    jet_pt = getattr(tree, "AntiKt4emtopoCalo422Jets_pt")
    jet_eta = getattr(tree, "AntiKt4emtopoCalo422Jets_eta")
    jet_phi = getattr(tree, "AntiKt4emtopoCalo422Jets_phi") 
    jet_m = getattr(tree, "AntiKt4emtopoCalo422Jets_m")
    #jetMass = getattr(tree, "AntiKt4emtopoCalo422JetsMass")


    max_pt_index = -1
    max_pt = -1
    for j in range(len(jet_pt)):
        if jet_pt[j] > max_pt:
            max_pt = jet_pt[j]
            max_pt_index = j 


    if max_pt_index != -1:
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(jet_pt[max_pt_index], jet_eta[max_pt_index], jet_phi[max_pt_index], jet_m[max_pt_index])
        hist_jet_pt.Fill(jet.Pt())
        hist_jet_eta.Fill(jet.Eta())
        hist_jet_phi.Fill(jet.Phi())
        hist_jet_m.Fill(jet.M()) 
        #hist_jetMass.Fill(jet.M())

print("Number of entries in the tree:", nEntries) 

canvas_jet = ROOT.TCanvas("canvas_jetMass", "Most Energetic Jet Count")
hist_jet_pt.Draw()
canvas_jet.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/plots_jetMass1.bay.pdf") 
root_file.Close()
 