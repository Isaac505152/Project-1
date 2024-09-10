import ROOT    #Script for pt of most energetic bquark and jet on same histogram
ROOT.gStyle.SetOptStat(0) 
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

hist_pt = ROOT.TH1F("hist_pt", "Pt of Most Energetic Jet and b-quark; p_{T} [GeV]; Events", 100, 0, 1000000)
hist_pt.SetLineColor(ROOT.kRed)  # Jet color
hist_pt.SetFillColor(ROOT.kRed)
hist_pt.SetFillStyle(3003)

hist_bquark_pt = ROOT.TH1F("hist_bquark_pt", "", 100, 0, 1000000)
hist_bquark_pt.SetLineColor(ROOT.kBlue)  # b-quark color
hist_bquark_pt.SetFillColor(ROOT.kBlue)
hist_bquark_pt.SetFillStyle(3004)


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

    
    if jet_pt:
        max_pt_jet = max(jet_pt)
        hist_pt.Fill(max_pt_jet)

    
    bquark = []
    for i in range(len(parts_pt)):
        if abs(parts_id[i]) == 5:
            part = ROOT.TLorentzVector()
            part.SetPtEtaPhiM(parts_pt[i], parts_eta[i], parts_phi[i], 4.18)
            if not any(part.DeltaR(b) < 0.5 and abs(part.Pt() - b.Pt()) < 20 for b in bquark):
                bquark.append(part)

    if bquark:
        most_energetic_bquark = max(bquark, key=lambda b: b.Pt())
        hist_bquark_pt.Fill(most_energetic_bquark.Pt())


canvas = ROOT.TCanvas("canvas", "Jet and b-quark Pt Analysis", 800, 600)
hist_pt.Draw("hist")
hist_bquark_pt.Draw("hist same")  # Draw on the same histogram

# Add legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(hist_pt, "Most Energetic Jet", "f")
legend.AddEntry(hist_bquark_pt, "Most Energetic b-quark", "f")
legend.Draw()

# Save the canvas
canvas.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_combined.pdf")

# Close the file
root_file.Close()




