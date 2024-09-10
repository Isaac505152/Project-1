import ROOT #Script showing pt of most energetic bquark and jet on different histograms
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


hist_jet_pt = ROOT.TH1F("hist_jet_pt", "Pt of Most Energetic Jet; p_{T} [GeV]; Events", 100, 0, 1000000)
hist_bquark_pt = ROOT.TH1F("hist_bquark_pt", "Pt of Most Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 1000000)


nEntries = tree.GetEntries()
for entryNum in range(nEntries):
    tree.GetEntry(entryNum)

    jet_pt = getattr(tree, "AntiKt4emtopoCalo422Jets_pt")
    jet_eta = getattr(tree, "AntiKt4emtopoCalo422Jets_eta")
    jet_phi = getattr(tree, "AntiKt4emtopoCalo422Jets_phi")
    jet_m = getattr(tree, "AntiKt4emtopoCalo422Jets_m")


    parts_pt = getattr(tree, "parts_pt")
    parts_eta = getattr(tree, "parts_eta")
    parts_phi = getattr(tree, "parts_phi")
    parts_id = getattr(tree, "parts_id")

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

    bquark = []
    for i in range(len(parts_pt)):
        if abs(parts_id[i]) == 5:
            part = ROOT.TLorentzVector()
            part.SetPtEtaPhiM(parts_pt[i], parts_eta[i], parts_phi[i], 4.18)
            if not any(part.DeltaR(b) < 0.5 and abs(part.Pt() - b.Pt()) < 20 for b in bquark):
                bquark.append(part)

    if len(bquark) ==4: 
        most_energetic_bquark = max(bquark, key=lambda b: b.Pt())
        hist_bquark_pt.Fill(most_energetic_bquark.Pt())


canvas = ROOT.TCanvas("canvas", "Jet and b-quark Pt Analysis", 800, 600)
canvas.Divide(2, 1)
canvas.cd(1)
hist_jet_pt.SetLineColor(ROOT.kRed)
hist_jet_pt.Draw()
canvas.cd(2)
hist_bquark_pt.SetLineColor(ROOT.kBlue)
hist_bquark_pt.Draw()


canvas.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_analysis.pdf")


root_file.Close() 

