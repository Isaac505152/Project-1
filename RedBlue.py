import ROOT               #Script for pt of 1st, 2nd most energetic jet and bquark
ROOT.gStyle.SetOptStat(1) 
import sys

file_path1 = "/Users/isaacanokye/Desktop/USATLAS24/game.root"
root_file1 = ROOT.TFile.Open(file_path1)

file_path2 = "/Users/isaacanokye/Desktop/USATLAS24/bay.root"
root_file2 = ROOT.TFile.Open(file_path2) 

if not root_file1 or root_file1.IsZombie(): 
    print("Error: Failed to open ROOT file.")
    sys.exit(1)

if not root_file2 or root_file2.IsZombie():
    print("Error: Failed to open ROOT file.")
    sys.exit(1)

tree1 = root_file1.Get("ntuple") 
if not tree1:
    print("Error: Tree not found in the file.")
    sys.exit(1) 

tree2 = root_file2.Get("ntuple")
if not tree2:
    print("Error: Tree not found in the file.")
    sys.exit(1)


hist_pt = ROOT.TH1F("hist_pt", "Pt of the Highest Jets from R&B; p_{T} [GeV]; Events", 100, 0, 400000)
hist_pt.SetLineColor(ROOT.kRed)
hist_pt.SetFillColor(ROOT.kRed)
hist_pt.SetFillStyle(3003)

hist_pt1 = ROOT.TH1F("hist_bquark_pt1", "Pt of the Highest Jets from R&B; p_{T} [GeV]; Events", 100, 0, 400000)
hist_pt1.SetLineColor(ROOT.kBlue)
hist_pt1.SetFillColor(ROOT.kBlue)
hist_pt1.SetFillStyle(3004)


hist_jet_pt1 = ROOT.TH1F("hist_jet_pt", "Pt of 2nd the Highest Jets from R&B; p_{T} [GeV]; Events", 100, 0, 400000)
hist_jet_pt1.SetLineColor(ROOT.kRed)
hist_jet_pt1.SetFillColor(ROOT.kRed)
hist_jet_pt1.SetFillStyle(3003)

hist_pt2 = ROOT.TH1F("hist_bquark_pt2", "Pt of the 2nd Highest Jets from R&B; p_{T} [GeV]; Events", 100, 0, 400000) 
hist_pt2.SetLineColor(ROOT.kBlue)
hist_pt2.SetFillColor(ROOT.kBlue)
hist_pt2.SetFillStyle(3004) 

hist_jet_pt3 = ROOT.TH1F("hist_jet_pt", "Pt of the 3rd Highest Jets from R&B; p_{T} [GeV]; Events", 100, 0, 400000)
hist_jet_pt3.SetLineColor(ROOT.kRed)
hist_jet_pt3.SetFillColor(ROOT.kRed)
hist_jet_pt3.SetFillStyle(3003)

hist_pt3 = ROOT.TH1F("hist_bquark_pt2", "Pt of the 3rd Highest Jets from R&B; p_{T} [GeV]; Events", 100, 0, 400000) 
hist_pt3.SetLineColor(ROOT.kBlue)
hist_pt3.SetFillColor(ROOT.kBlue)
hist_pt3.SetFillStyle(3004)

hist_jet_pt4 = ROOT.TH1F("hist_jet_pt", "Pt of the 1st & 4th Highest Jets from R&B; p_{T} [GeV]; Events", 100, 0, 400000)
hist_jet_pt4.SetLineColor(ROOT.kRed)
hist_jet_pt4.SetFillColor(ROOT.kRed)
hist_jet_pt4.SetFillStyle(3003)

hist_pt4 = ROOT.TH1F("hist_bquark_pt2", "Pt of the 1st & 4th Highest Jets from R&B; p_{T} [GeV]; Events", 100, 0, 400000) 
hist_pt4.SetLineColor(ROOT.kBlue)
hist_pt4.SetFillColor(ROOT.kBlue)
hist_pt4.SetFillStyle(3004)



nEntries = tree1.GetEntries()
for entryNum in range(nEntries):
    tree1.GetEntry(entryNum)
    
    parts_pt = getattr(tree1, "parts_pt")
    parts_eta = getattr(tree1, "parts_eta")
    parts_phi = getattr(tree1, "parts_phi")
    parts_id = getattr(tree1, "parts_id") 
    jet_pt = getattr(tree1, "AntiKt4emtopoCalo422Jets_pt")
    jet_eta = getattr(tree1, "AntiKt4emtopoCalo422Jets_eta")
    jet_phi = getattr(tree1, "AntiKt4emtopoCalo422Jets_phi")
    jet_m = getattr(tree1, "AntiKt4emtopoCalo422Jets_m")  
    

    
    jets = [ROOT.TLorentzVector() for pt, eta, phi, m in zip(jet_pt, jet_eta, jet_phi, jet_m)]
    for j, (pt, eta, phi, m) in enumerate(zip(jet_pt, jet_eta, jet_phi, jet_m)):
        jets[j].SetPtEtaPhiM(pt, eta, phi, m)
    jets.sort(key=lambda x: x.Pt(), reverse=True) 

    
    if jets:
        hist_pt.Fill(jets[0].Pt())
        #if len(jets) > 1:
           # hist_jet_pt1.Fill(jets[1].Pt())
            #if len(jets) > 2:
                #hist_jet_pt3.Fill(jets[2].Pt()) 
                #if len(jets) > 3:
                    #hist_jet_pt4.Fill(jets[3].Pt()) 

nEntries = tree2.GetEntries()
for entryNum in range(nEntries):
    tree2.GetEntry(entryNum)  
    
    parts_pt = getattr(tree2, "parts_pt")
    parts_eta = getattr(tree2, "parts_eta")
    parts_phi = getattr(tree2, "parts_phi")
    parts_id = getattr(tree2, "parts_id") 
    jet_pt = getattr(tree2, "AntiKt4emtopoCalo422Jets_pt")
    jet_eta = getattr(tree2, "AntiKt4emtopoCalo422Jets_eta")
    jet_phi = getattr(tree2, "AntiKt4emtopoCalo422Jets_phi")
    jet_m = getattr(tree2, "AntiKt4emtopoCalo422Jets_m") 
    

    
    jets = [ROOT.TLorentzVector() for pt, eta, phi, m in zip(jet_pt, jet_eta, jet_phi, jet_m)]
    for j, (pt, eta, phi, m) in enumerate(zip(jet_pt, jet_eta, jet_phi, jet_m)):
        jets[j].SetPtEtaPhiM(pt, eta, phi, m)
    jets.sort(key=lambda x: x.Pt(), reverse=True) 

    
    #if jets:
        #hist_pt1.Fill(jets[0].Pt())
        #if len(jets) > 1:
           # hist_pt2.Fill(jets[1].Pt())
            #if len(jets) > 2:
               # hist_pt3.Fill(jets[2].Pt())   
    if len(jets) > 3: 
        hist_pt4.Fill(jets[3].Pt()) 

#canvas1 = ROOT.TCanvas("canvas1", "Highest R & B jets ", 800, 600)
#hist_pt.Draw("hist")
#hist_pt1.Draw("hist same")
#legend1 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
#legend1.AddEntry(hist_pt, "Highest jets from R", "f")
#legend1.AddEntry(hist_pt1, "Highest jets from B", "f")
#legend1.Draw()
#canvas1.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_1st.R&B.pdf")  


#canvas2 = ROOT.TCanvas("canvas2", "2nd Highest R & B jets", 800, 600)
#hist_jet_pt1.Draw("hist")
#hist_pt2.Draw("hist same")
#legend2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
#legend2.AddEntry(hist_jet_pt1, "2nd Highest jets from R", "f")
#legend2.AddEntry(hist_pt2, "2nd Highest jets from B", "f")
#legend2.Draw()
#canvas2.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_2nd.R&B.pdf")  

#canvas3 = ROOT.TCanvas("canvas3", "3rd Highest R & B jets", 800, 600)
#hist_pt.Draw("hist")
#hist_pt2.Draw("hist same")
#legend3 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
#legend3.AddEntry(hist_jet_pt3, "3rd Highest jets from R", "f")
#legend3.AddEntry(hist_pt3, "3rd Highest jets from B", "f")
#legend3.Draw()
#canvas3.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_3rd.R&B.pdf") 

#canvas4 = ROOT.TCanvas("canvas4", "4th Highest R & B jets", 800, 600)
#hist_jet_pt4.Draw("hist")
#hist_pt4.Draw("hist same")
#legend4 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
#legend4.AddEntry(hist_jet_pt4, "4th Highest jets from R", "f")
#legend4.AddEntry(hist_pt4, "4th Highest jets from B", "f")
#legend4.Draw()
#canvas4.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_4th.R&B.pdf")

canvasb = ROOT.TCanvas("canvas4", "1st & 4th Highest R & B jets", 800, 600)
hist_pt4.Draw("hist")
hist_pt.Draw("hist same")
legendb = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legendb.AddEntry(hist_pt, "1st Highest jets from R", "f")
legendb.AddEntry(hist_pt4,"4th Highest jets from B", "f")
legendb.Draw()
canvasb.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_4th.R&B.pdf")
root_file1.Close() 
root_file2.Close()  


#R=game.root file = file1
#B=bay.root file=file 2