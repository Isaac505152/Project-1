import ROOT  #Scripts for Invariant Mass of b-quarks & Jets 
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


hist_pt = ROOT.TH1F("hist_pt", "Transverse Momentum; p_{T} [GeV]; Events", 100, 0, 200000)
hist_bquark_count = ROOT.TH1F("hist_bquark_count", "Number of Bottom Quarks per Event; Number of b-quarks; Events", 10, 0, 10) 
hist_pt_duplicate = ROOT.TH1F("hist_pt_duplicate", "Transverse Momentum of Duplicate b-quarks; p_{T} [GeV]; Events", 100, 0, 200000) 
hist_bquark_mass = ROOT.TH1F("hist_bquark_mass", "Invariant Mass of b-quarks & Jets; Mass [GeV]; Events", 100, 0, 1000000)  
hist_bquark_mass.SetLineColor(2) 

hist_jet_pt = ROOT.TH1F("hist_jet_pt", "Transverse Momentum of Jets; p_{T} [GeV]; Events", 100, 0, 2000)
hist_jet_eta = ROOT.TH1F("hist_jet_eta", "Pseudorapidity of Jets; eta; Events", 100, 0, 10)
hist_jet_phi = ROOT.TH1F("hist_jet_phi", "Azimuthal Angle of Jets; phi; Events", 100, 0, 360)
hist_jet_m = ROOT.TH1F("hist_jet_m", "Mass of Jets; m [GeV]; Events", 100, 0, 200)
hist_jetMass = ROOT.TH1F("hist_jetMass", "Invariant mass of First Four Jets; Mass [GeV]; Events", 100, 0, 1000000)


pdf_file_path = "/Users/isaacanokye/Desktop/USATLAS24/combined_quarks_and_jets.bay.pdf" 
pdf = ROOT.TPDF(pdf_file_path, 111)


nEntries = tree.GetEntries()
for entryNum in range(nEntries): 
    tree.GetEntry(entryNum)

    
    pt = getattr(tree, "parts_pt")
    eta = getattr(tree, "parts_eta") 
    phi = getattr(tree, "parts_phi") 
    iddi = getattr(tree, "parts_id") 
    jet_pt = getattr(tree, "AntiKt4emtopoCalo422Jets_pt") 
    jet_eta = getattr(tree, "AntiKt4emtopoCalo422Jets_eta")
    jet_phi = getattr(tree, "AntiKt4emtopoCalo422Jets_phi")
    jet_m = getattr(tree, "AntiKt4emtopoCalo422Jets_m")

    
    bquark_count = 0
    bquark = []
    for i in range(len(pt)):
        part = ROOT.TLorentzVector()
        part.SetPtEtaPhiM(pt[i], eta[i], phi[i], 4.18)

        duplicate = False
        for b in bquark:
            if part.DeltaR(b) < 0.5 and abs(part.Pt() - b.Pt()) < 100000:
                duplicate = True
                hist_pt_duplicate.Fill(pt[i])

        if abs(iddi[i]) == 5 and not duplicate:
            bquark.append(part)
            bquark_count += 1

    if bquark_count == 4:
        bquark_system = bquark[0] + bquark[1] + bquark[2] + bquark[3]
        bquarkMass = bquark_system.M()
        hist_bquark_mass.Fill(bquarkMass)

    hist_bquark_count.Fill(bquark_count) 

    
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


canvas = ROOT.TCanvas("canvas", "Plots")

hist_bquark_mass.Draw()
hist_jetMass.Draw("same")
canvas.Print(pdf_file_path)


#bquark=red
#jet= blue


pdf.Close()
root_file.Close()

 







