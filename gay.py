import ROOT         
ROOT.gStyle.SetOptStat(1) 
import sys

file_path1 = "/Users/isaacanokye/Desktop/USATLAS24/game.root"
root_file1 = ROOT.TFile.Open(file_path1)


if not root_file1 or root_file1.IsZombie():
    print("Error: Failed to open ROOT file.")
    sys.exit(1)


tree1 = root_file1.Get("ntuple")
if not tree1:
    print("Error: Tree not found in the file.")
    sys.exit(1)


hist_pt = ROOT.TH1F("hist_pt", "Pt of the 1st Highest Jet; p_{T} [GeV]; Events", 100, 0, 400000)
hist_pt.SetLineColor(ROOT.kRed)
hist_pt.SetFillColor(ROOT.kRed)
hist_pt.SetFillStyle(3003)

hist_jet_pt = ROOT.TH1F("hist_jet_pt", "Pt of 1st & 4th Highest Jets from HH->4b; p_{T} [GeV]; Events", 100, 0, 400000)
hist_jet_pt.SetLineColor(ROOT.kBlue)
hist_jet_pt.SetFillColor(ROOT.kBlue)
hist_jet_pt.SetFillStyle(3003)

hist_ratio = ROOT.TH1F("hist_ratio", "Ratio of Pt of 1st Jet to 4th Jet; p_{T} Ratio; Events", 100, 0, 10)
hist_ratio.SetLineColor(ROOT.kRed)
hist_ratio.SetFillColor(ROOT.kBlue)
hist_ratio.SetFillStyle(3003)

nEntries = tree1.GetEntries()
for entryNum in range(nEntries):
    tree1.GetEntry(entryNum)
    
    jet_pt = getattr(tree1, "AntiKt4emtopoCalo422Jets_pt")
    jet_eta = getattr(tree1, "AntiKt4emtopoCalo422Jets_eta")
    jet_phi = getattr(tree1, "AntiKt4emtopoCalo422Jets_phi")
    jet_m = getattr(tree1, "AntiKt4emtopoCalo422Jets_m")

    jets = [ROOT.TLorentzVector() for _ in range(len(jet_pt))]
    for i in range(len(jet_pt)):
        jets[i].SetPtEtaPhiM(jet_pt[i], jet_eta[i], jet_phi[i], jet_m[i])
    jets.sort(key=lambda x: x.Pt(), reverse=True)


    #if len(jets) > 0:
     #   hist_pt.Fill(jets[0].Pt())
    #if len(jets) > 3:
     #   hist_jet_pt.Fill(jets[3].Pt())
    if len(jets) > 3:
        pt_first_jet = jets[0].Pt() if len(jets) > 0 else 0  
        pt_fourth_jet = jets[3].Pt() 
        
        if pt_fourth_jet > 0:  
            pt_ratio = pt_first_jet / pt_fourth_jet
            hist_ratio.Fill(pt_ratio)



canvas4 = ROOT.TCanvas("canvas4", "1st & 4th Highest Jet from R & B", 800, 600)
hist_jet_pt.Draw("hist")
hist_pt.Draw("hist same")
legend4 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend4.AddEntry(hist_jet_pt, "4th Highest Jet", "f")
legend4.AddEntry(hist_pt, "1st Highest jet", "f")
legend4.Draw()
canvas4.SaveAs("/Users/isaacanokye/Desktop/USATLAS24/jet_bquark_pt_1st_4th_jets.pdf")


root_file1.Close()
