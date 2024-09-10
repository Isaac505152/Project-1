import ROOT #Script for Eta of 1st-4th most energetic b-quark and Jet
ROOT.gStyle.SetOptStat(0)  
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

hist_eta = ROOT.TH1F("hist_eta", "Eta of Most Energetic Jet and b-quark; eta; Events", 40, -5, 5)
hist_eta.SetLineColor(ROOT.kRed)
hist_eta.SetFillColor(ROOT.kRed)
hist_eta.SetFillStyle(3003)

hist_bquark_eta1 = ROOT.TH1F("hist_bquark_eta1", "Eta of Most Energetic b-quark; eta; Events", 60, -5, 5)
hist_bquark_eta1.SetLineColor(ROOT.kBlue)
hist_bquark_eta1.SetFillColor(ROOT.kBlue) 
hist_bquark_eta1.SetFillStyle(3004)

hist_jet_eta = ROOT.TH1F("hist_jet_eta", "Eta of 2nd Most Energetic b-quark & Jet; eta; Events", 60, -5, 5)
hist_jet_eta.SetLineColor(ROOT.kRed)
hist_jet_eta.SetFillColor(ROOT.kRed)
hist_jet_eta.SetFillStyle(3003)

hist_bquark_eta2 = ROOT.TH1F("hist_bquark_eta2", "Eta of 2nd Most Energetic b-quark; eta; Events", 60, -5, 5)
hist_bquark_eta2.SetLineColor(ROOT.kBlue)
hist_bquark_eta2.SetFillColor(ROOT.kBlue)
hist_bquark_eta2.SetFillStyle(3004)

hist_eta3 = ROOT.TH1F("hist_eta3", "Eta of 3rd Most Energetic Jet and b-quark; eta; Events", 60, -5, 5)
hist_eta3.SetLineColor(ROOT.kRed)
hist_eta3.SetFillColor(ROOT.kRed)
hist_eta3.SetFillStyle(3003)

hist_bquark_eta3 = ROOT.TH1F("hist_bquark_eta3", "Eta of 3rd Most Energetic b-quark; eta; Events", 60, -5, 5)
hist_bquark_eta3.SetLineColor(ROOT.kBlue)
hist_bquark_eta3.SetFillColor(ROOT.kBlue)
hist_bquark_eta3.SetFillStyle(3004)

hist_eta4 = ROOT.TH1F("hist_eta4", "Eta of 4th Energetic Jet and b-quark; eta; Events", 60, -5, 5)
hist_eta4.SetLineColor(ROOT.kRed)
hist_eta4.SetFillColor(ROOT.kRed)
hist_eta4.SetFillStyle(3003)

hist_bquark_eta4 = ROOT.TH1F("hist_bquark_eta4", "Eta of 4th Energetic b-quark; eta; Events", 40, -5, 5) 
hist_bquark_eta4.SetLineColor(ROOT.kBlue) 
hist_bquark_eta4.SetFillColor(ROOT.kBlue)
hist_bquark_eta4.SetFillStyle(3004)

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
    for i in range(len(parts_eta)):
        if abs(parts_id[i]) == 5:
            part = ROOT.TLorentzVector()
            part.SetPtEtaPhiM(parts_pt[i], parts_eta[i], parts_phi[i], 4.18)
            if not any(part.DeltaR(b) < 0.5 and abs(part.Pt() - b.Eta()) < 20 for b in bquarks):
                bquarks.append(part) 
    bquarks.sort(key=lambda b: b.Pt(), reverse=True) 


    if jets:
       hist_eta.Fill(jets[0].Eta())
       if len(jets) > 1:
           hist_jet_eta.Fill(jets[1].Eta())
           if len(jets) > 2:
               hist_eta3.Fill(jets[2].Eta())
               if len(jets) > 3:
                   hist_eta4.Fill(jets[3].Eta())
    if bquarks:
        hist_bquark_eta1.Fill(bquarks[0].Eta())
        if len(bquarks) > 1:
           hist_bquark_eta2.Fill(bquarks[1].Eta())
           if len(bquarks) > 2:
               hist_bquark_eta3.Fill(bquarks[2].Eta())
               if len(bquarks) > 3:
                   hist_bquark_eta4.Fill(bquarks[3].Eta()) 

canvas1 = ROOT.TCanvas("canvas1", "Most Energetic Jet and b-quark", 800, 600)
hist_eta.Draw("hist")
hist_bquark_eta1.Draw("hist same")
legend1 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend1.AddEntry(hist_eta, "Most Energetic Jet", "f")
legend1.AddEntry(hist_bquark_eta1, "Most Energetic b-quark", "f")
legend1.Draw()
canvas1.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_1st_eta.bay.pdf")

canvas2 = ROOT.TCanvas("canvas2", "2nd Most Energetic Jet and b-quark", 800, 600)
hist_jet_eta.Draw("hist")
hist_bquark_eta2.Draw("hist same") 
legend2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend2.AddEntry(hist_jet_eta, "2nd Most Energetic Jet", "f")
legend2.AddEntry(hist_bquark_eta2, "2nd Most Energetic b-quark", "f")
legend2.Draw()
canvas2.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_2nd_eta.bay.pdf") 

canvas3 = ROOT.TCanvas("canvas3", "3rd Most Energetic Jet and b-quark", 800, 600)
hist_eta3.Draw("hist") 
hist_bquark_eta3.Draw("hist same")
legend3 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend3.AddEntry(hist_eta3, "3rd Most Energetic Jet", "f")
legend3.AddEntry(hist_bquark_eta3, "3rd Most Energetic b-quark", "f") 
legend3.Draw()
canvas3.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_3rd_eta.bay.pdf")  

canvas4 = ROOT.TCanvas("canvas4", "4th Energetic Jet and b-quark", 800, 600)
hist_eta4.Draw("hist") 
hist_bquark_eta4.Draw("hist same")
legend4 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend4.AddEntry(hist_eta4, "4th Energetic Jet", "f")
legend4.AddEntry(hist_bquark_eta4, "4th Energetic b-quark", "f")  
legend4.Draw()
canvas4.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_4th_eta.bay.pdf")
  

root_file.Close()   




