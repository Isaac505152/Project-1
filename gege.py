import ROOT #Scripts for Pt of 1st-4th most energetic b-quark and jet  
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


hist_pt = ROOT.TH1F("hist_pt", "Pt of Most Energetic Jet and b-quark; p_{T} [GeV]; Events", 100, 0, 4000)
hist_pt.SetLineColor(ROOT.kRed)
hist_pt.SetFillColor(ROOT.kRed)
hist_pt.SetFillStyle(3003)

hist_bquark_pt1 = ROOT.TH1F("hist_bquark_pt1", "Pt of Most Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 400)
hist_bquark_pt1.SetLineColor(ROOT.kBlue)
hist_bquark_pt1.SetFillColor(ROOT.kBlue)
hist_bquark_pt1.SetFillStyle(3004)


hist_jet_pt = ROOT.TH1F("hist_jet_pt", "Pt of 2nd Most Energetic b-quark & Jet; p_{T} [GeV]; Events", 100, 0, 400)
hist_jet_pt.SetLineColor(ROOT.kRed)
hist_jet_pt.SetFillColor(ROOT.kRed)
hist_jet_pt.SetFillStyle(3003)

hist_bquark_pt2 = ROOT.TH1F("hist_bquark_pt2", "Pt of 2nd Most Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 4000) 
hist_bquark_pt2.SetLineColor(ROOT.kBlue)
hist_bquark_pt2.SetFillColor(ROOT.kBlue)
hist_bquark_pt2.SetFillStyle(3004)

hist_pt3 = ROOT.TH1F("hist_pt3", "Pt of 3rd Most Energetic Jet and b-quark; p_{T} [GeV]; Events", 100, 0, 4000)
hist_pt3.SetLineColor(ROOT.kRed)
hist_pt3.SetFillColor(ROOT.kRed)
hist_pt3.SetFillStyle(3003)

hist_bquark_pt3 = ROOT.TH1F("hist_bquark_pt3", "Pt of 3rd Most Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 4000)
hist_bquark_pt3.SetLineColor(ROOT.kBlue)
hist_bquark_pt3.SetFillColor(ROOT.kBlue)
hist_bquark_pt3.SetFillStyle(3004)

hist_pt4 = ROOT.TH1F("hist_pt4", "Pt of 4th Energetic Jet and b-quark; p_{T} [GeV]; Events", 100, 0, 4000)
hist_pt4.SetLineColor(ROOT.kRed)
hist_pt4.SetFillColor(ROOT.kRed)
hist_pt4.SetFillStyle(3003)

hist_bquark_pt4 = ROOT.TH1F("hist_bquark_pt4", "Pt of 4th Energetic b-quark; p_{T} [GeV]; Events", 100, 0, 400)
hist_bquark_pt4.SetLineColor(ROOT.kBlue)
hist_bquark_pt4.SetFillColor(ROOT.kBlue)
hist_bquark_pt4.SetFillStyle(3004)  

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

     
    bquarks = []
    for i in range(len(parts_pt)):
        if abs(parts_id[i]) == 5:
            part = ROOT.TLorentzVector()
            part.SetPtEtaPhiM(parts_pt[i], parts_eta[i], parts_phi[i], 4.18)
            if not any(part.DeltaR(b) < 0.5 and abs(part.Pt() - b.Pt()) < 20 for b in bquarks):
                bquarks.append(part)
    bquarks.sort(key=lambda b: b.Pt(), reverse=True)

    
    if jets:
        hist_pt.Fill(jets[0].Pt())
        if len(jets) > 1:
            hist_jet_pt.Fill(jets[1].Pt())
            if len(jets) > 2:
                hist_pt3.Fill(jets[2].Pt())
                if len(jets) > 3:
                    hist_pt4.Fill(jets[3].Pt())  
    if bquarks:
        hist_bquark_pt1.Fill(bquarks[0].Pt())
        if len(bquarks) > 1:
            hist_bquark_pt2.Fill(bquarks[1].Pt())
            if len(bquarks) > 2:
                hist_bquark_pt3.Fill(bquarks[2].Pt()) 
                if len(bquarks) > 3:
                    hist_bquark_pt4.Fill(bquarks[3].Pt()) 


canvas1 = ROOT.TCanvas("canvas1", "Most Energetic Jet and b-quark", 800, 600)
hist_pt.Draw("hist")
hist_bquark_pt1.Draw("hist same")
legend1 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend1.AddEntry(hist_pt, "Most Energetic Jet", "f")
legend1.AddEntry(hist_bquark_pt1, "Most Energetic b-quark", "f")
legend1.Draw()
canvas1.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_1st_pt.pdf")


canvas2 = ROOT.TCanvas("canvas2", "2nd Most Energetic Jet and b-quark", 800, 600)
hist_jet_pt.Draw("hist")
hist_bquark_pt2.Draw("hist same")
legend2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend2.AddEntry(hist_jet_pt, "2nd Most Energetic Jet", "f")
legend2.AddEntry(hist_bquark_pt2, "2nd Most Energetic b-quark", "f")
legend2.Draw()
canvas2.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_2nd_pt.pdf") 

canvas3 = ROOT.TCanvas("canvas3", "3rd Most Energetic Jet and b-quark", 800, 600)
hist_pt3.Draw("hist") 
hist_bquark_pt3.Draw("hist same")
legend3 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend3.AddEntry(hist_pt3, "3rd Most Energetic Jet", "f")
legend3.AddEntry(hist_bquark_pt3, "3rd Most Energetic b-quark", "f") 
legend3.Draw()
canvas3.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_3rd_pt.pdf")  

canvas4 = ROOT.TCanvas("canvas4", "4th Energetic Jet and b-quark", 800, 600)
hist_pt4.Draw("hist") 
hist_bquark_pt4.Draw("hist same")
legend4 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend4.AddEntry(hist_pt4, "4th Energetic Jet", "f")
legend4.AddEntry(hist_bquark_pt4, "4th Energetic b-quark", "f")  
legend4.Draw()
canvas4.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_4th_pt.pdf") 

root_file.Close()  



