import ROOT             
ROOT.gStyle.SetOptStat(0) 
import sys

file_path2 = "/Users/isaacanokye/Desktop/USATLAS24/bay.root"
root_file2 = ROOT.TFile.Open(file_path2) 


if not root_file2 or root_file2.IsZombie():
    print("Error: Failed to open ROOT file.")
    sys.exit(1)


tree2 = root_file2.Get("ntuple")
if not tree2:
    print("Error: Tree not found in the file.")
    sys.exit(1)


hist_pt = ROOT.TH1F("hist_pt", "Pt of Most Energetic Jet and b-quark; p_{T} [GeV]; Events", 100, 0, 400000)
hist_pt.SetLineColor(ROOT.kBlue)
hist_pt.SetFillColor(ROOT.kBlue)
hist_pt.SetFillStyle(3003)

hist_bquark_pt1 = ROOT.TH1F("hist_bquark_pt1", "Pt of Most Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 400000)
hist_bquark_pt1.SetLineColor(ROOT.kRed)
hist_bquark_pt1.SetFillColor(ROOT.kRed)
hist_bquark_pt1.SetFillStyle(3004)


hist_jet_pt = ROOT.TH1F("hist_jet_pt", "Pt of 2nd Most Energetic b-quark & Jet; p_{T} [GeV]; Events", 100, 0, 400000)
hist_jet_pt.SetLineColor(ROOT.kBlue)
hist_jet_pt.SetFillColor(ROOT.kBlue)
hist_jet_pt.SetFillStyle(3003)

hist_bquark_pt2 = ROOT.TH1F("hist_bquark_pt2", "Pt of 2nd Most Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 400000) 
hist_bquark_pt2.SetLineColor(ROOT.kRed)
hist_bquark_pt2.SetFillColor(ROOT.kRed)
hist_bquark_pt2.SetFillStyle(3004)

hist_jet_pt3 = ROOT.TH1F("hist_jet_pt", "Pt of 2nd Most Energetic b-quark & Jet; p_{T} [GeV]; Events", 100, 0, 400000)
hist_jet_pt3.SetLineColor(ROOT.kBlue)
hist_jet_pt3.SetFillColor(ROOT.kBlue)
hist_jet_pt3.SetFillStyle(3003)

hist_bquark_pt3 = ROOT.TH1F("hist_bquark_pt2", "Pt of 2nd Most Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 400000) 
hist_bquark_pt3.SetLineColor(ROOT.kRed)
hist_bquark_pt3.SetFillColor(ROOT.kRed) 
hist_bquark_pt3.SetFillStyle(3004)


nEntries = tree.GetEntries()
for entryNum in range(nEntries):
    tree.GetEntry(entryNum)
    
    parts_pt = getattr(tree, "parts_pt")
    parts_eta = getattr(tree, "parts_eta")
    parts_phi = getattr(tree, "parts_phi")
    parts_id = getattr(tree, "parts_id") 
    jet_pt = getattr(tree, "AntiKt4emtopoCalo422Jets_pt")
    jet_eta = getattr(tree, "AntiKt4emtopoCalo422Jets_eta")
    jet_phi = getattr(tree, "AntiKt4emtopoCalo422Jets_phi")
    jet_m = getattr(tree, "AntiKt4emtopoCalo422Jets_m") 
    

    
    jets = [ROOT.TLorentzVector() for pt, eta, phi, m in zip(jet_pt, jet_eta, jet_phi, jet_m)]
    for j, (pt, eta, phi, m) in enumerate(zip(jet_pt, jet_eta, jet_phi, jet_m)):
        jets[j].SetPtEtaPhiM(pt, eta, phi, m)
    jets.sort(key=lambda x: x.Pt(), reverse=True) 

    
    if jets:
        hist_pt.Fill(jets[0].Pt())
        if len(jets) > 1:
            hist_jet_pt.Fill(jets[1].Pt())
            if len(jets) > 2:
                hist_jet_pt.Fill(jets[2].Pt()) 
        

canvas1 = ROOT.TCanvas("canvas1", "Most Energetic Jet and b-quark", 800, 600)
hist_pt.Draw("hist")
hist_bquark_pt1.Draw("hist same")
legend1 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend1.AddEntry(hist_pt, "Most Energetic Jet", "f")
legend1.AddEntry(hist_bquark_pt1, "Most Energetic b-quark", "f")
legend1.Draw()
canvas1.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_1st.gu.pdf")  


canvas2 = ROOT.TCanvas("canvas2", "2nd Most Energetic Jet and b-quark", 800, 600)
hist_jet_pt.Draw("hist")
hist_bquark_pt2.Draw("hist same")
legend2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend2.AddEntry(hist_jet_pt, "2nd Most Energetic Jet", "f")
legend2.AddEntry(hist_bquark_pt2, "2nd Most Energetic b-quark", "f")
legend2.Draw()
canvas2.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_2nd.gu.pdf")  

canvas3 = ROOT.TCanvas("canvas3", "3rd Most Energetic Jet and b-quark", 800, 600)
hist_jet_pt.Draw("hist")
hist_bquark_pt2.Draw("hist same")
legend3 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend3.AddEntry(hist_jet_pt3, "3rd Most Energetic Jet", "f")
legend3.AddEntry(hist_bquark_pt3, "3rd Most Energetic b-quark", "f")
legend3.Draw()
canvas3.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_3rd.gu.pdf")  

root_file2.Close() 