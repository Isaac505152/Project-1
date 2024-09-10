import ROOT  #Script for pt of the most energetic b quark 
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

pdf_file_path = "/Users/isaacanokye/Desktop/USATLAS24/most_energetic_bquark.bay.pdf"
pdf = ROOT.TPDF(pdf_file_path, 111)

hist_most_energetic_bquark_pt = ROOT.TH1F("hist_most_energetic_bquark_pt", "Pt of Most Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 1000000)

nEntries = tree.GetEntries()
for entryNum in range(nEntries):
    tree.GetEntry(entryNum)

    pt = getattr(tree, "parts_pt")
    eta = getattr(tree, "parts_eta")
    phi = getattr(tree, "parts_phi")
    iddi = getattr(tree, "parts_id")

    bquark = []
    for i in range(len(pt)):
        part = ROOT.TLorentzVector()
        part.SetPtEtaPhiM(pt[i], eta[i], phi[i], 4.18)

        duplicate = False
        for b in bquark:
            if part.DeltaR(b) < 0.5 and abs(part.Pt() - b.Pt()) < 100000:
                duplicate = True

        if abs(iddi[i]) == 5 and not duplicate:
            bquark.append(part)
        
        


    if len(bquark) ==4: 
        most_energetic_bquark = max(bquark, key=lambda b: b.Pt())
        hist_most_energetic_bquark_pt.Fill(most_energetic_bquark.Pt())

canvas = ROOT.TCanvas("canvas", "Most Energetic b-quark Plot", 800, 600)

hist_most_energetic_bquark_pt.SetLineColor(ROOT.kBlue)
hist_most_energetic_bquark_pt.Draw()

canvas.Print(pdf_file_path)

pdf.Close()
root_file.Close()



