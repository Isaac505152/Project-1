import ROOT
import sys

if len(sys.argv) != 3:
    print ("USAGE: %s <input file>  <output file>"% (sys.argv[0]))
    sys.exit(1) 

histFileName = sys.argv[1]
plotFileName = sys.argv[2] 

print ("Reading from", histFileName, "and writing to",plotFileName)  
histFile = ROOT.TFile.Open(histFileName ,"READ") 

dataHisto = histFile.Get("data") 
mcHisto = histFile.Get("mc") 

if not dataHisto:
    print ("Failed to get data histogram") 
    sys.exit(1) 
if not mcHisto: 
    print ("Failed to get MC histogram") 
    sys.exit(1) 

dataHisto.SetDirectory(0)  
mcHisto.SetDirectory(0) 
histFile.Close()

canvas = ROOT.TCanvas("canvas")
canvas.cd() 

canvas.Print(plotFileName+"[") 

mcHisto.Draw("h") 

canvas.Print(plotFileName) 

dataHisto.Draw("pe")
canvas.Print(plotFileName)  

mcHisto.SetStats(0) 
dataHisto.SetStats(0)
mcHisto.SetLineColor(ROOT.kRed) 
dataHisto.SetLineColor(ROOT.kBlack) 
mcHisto.SetLineWidth(2) 
dataHisto.SetLineWidth(2)

mcHisto.GetYaxis().SetTitle("Number of events") 
dataHisto.GetYaxis().SetTitle("Number of events") 
mcHisto.GetXaxis().SetTitle("m_{ll} [MeV]") 
dataHisto.GetXaxis().SetTitle("m_{ll} [MeV]") 
canvas.SetLogy(True) 

mcHisto.Scale(dataHisto.Integral()/mcHisto.Integral())

mcHisto.Draw("h")  
dataHisto.Draw("pe,same") 
canvas.Print(plotFileName) 

ratio = dataHisto.Clone() 
ratio.Divide(mcHisto) 
ratio.SetLineColor(ROOT.kRed)
canvas.Clear()

pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1) 
pad1.SetLogy(True)
pad1.Draw()
pad1.cd()
mcHisto.Draw("h") 
dataHisto.Draw("pe,same")

canvas.cd()
pad2 = ROOT.TPad("pad2","pad2",0,0.05,1,0.3) 
pad2.Draw()
pad2.cd()
ratio.Draw("pe")
canvas.Print(plotFileName) 

pad1.SetBottomMargin(0) 

pad2.SetTopMargin(0) 
pad2.SetBottomMargin(0.25)

mcHisto.SetTitle("") 
mcHisto.GetXaxis().SetLabelSize(0) 
mcHisto.GetXaxis().SetTitleSize(0)

mcHisto.GetYaxis().SetTitleSize(0.05)

ratio.SetTitle("") 
ratio.GetXaxis().SetLabelSize(0.12) 
ratio.GetXaxis().SetTitleSize(0.12) 
ratio.GetYaxis().SetLabelSize(0.1) 
ratio.GetYaxis().SetTitleSize(0.15) 
ratio.GetYaxis().SetTitle("Data/MC") 
ratio.GetYaxis().SetTitleOffset(0.3) 

ratio.GetYaxis().SetRangeUser(0.5,1.5)
ratio.GetYaxis().SetNdivisions(207)

line = ROOT.TLine(50.e3,1,200.e3,1) 
line.SetLineColor(ROOT.kBlack) 
line.SetLineWidth(2) 
line.Draw("same")

legend = ROOT.TLegend(0.7,0.6,0.85,0.75) 
legend.AddEntry(mcHisto ,"MC") 
legend.AddEntry(dataHisto ,"Data") 
legend.SetLineWidth(0) 
legend.Draw("same")

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.06) 
latex.DrawText(0.7,0.83,"HASCO 2018") 
latex.SetTextSize(0.04) 
latex.DrawText(0.7,0.77,"Di-muon events")
mcHisto.SetStats(0) 
dataHisto.SetStats(0)
mcHisto.SetLineColor(ROOT.kRed) 
dataHisto.SetLineColor(ROOT.kBlack) 
mcHisto.SetLineWidth(2) 
dataHisto.SetLineWidth(2)

mcHisto.GetYaxis().SetTitle("Number of events") 
dataHisto.GetYaxis().SetTitle("Number of events") 
mcHisto.GetXaxis().SetTitle("m_{ll} [MeV]") 
dataHisto.GetXaxis().SetTitle("m_{ll} [MeV]")

canvas.SetLogy(True)  
mcHisto.Scale(dataHisto.Integral()/mcHisto.Integral())

mcHisto.Draw("h") 
dataHisto.Draw("pe,same") 
canvas.Print(plotFileName) 
ratio = dataHisto.Clone() 
ratio.Divide(mcHisto) 
ratio.SetLineColor(ROOT.kRed)
canvas.Clear()

pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1) 
pad1.SetLogy(True)
pad1.Draw()
pad1.cd()
mcHisto.Draw("h") 
dataHisto.Draw("pe,same")

canvas.cd()
pad2 = ROOT.TPad("pad2","pad2",0,0.05,1,0.3) 
pad2.Draw()
pad2.cd()
ratio.Draw("pe")
canvas.Print(plotFileName) 

pad1.SetBottomMargin(0) 

pad2.SetTopMargin(0) 
pad2.SetBottomMargin(0.25)

mcHisto.SetTitle("") 
mcHisto.GetXaxis().SetLabelSize(0) 
mcHisto.GetXaxis().SetTitleSize(0)

mcHisto.GetYaxis().SetTitleSize(0.05)

ratio.SetTitle("") 
ratio.GetXaxis().SetLabelSize(0.12) 
ratio.GetXaxis().SetTitleSize(0.12) 
ratio.GetYaxis().SetLabelSize(0.1) 
ratio.GetYaxis().SetTitleSize(0.15) 
ratio.GetYaxis().SetTitle("Data/MC") 
ratio.GetYaxis().SetTitleOffset(0.3)

ratio.GetYaxis().SetRangeUser(0.5,1.5)
ratio.GetYaxis().SetNdivisions(207)

line = ROOT.TLine(50.e3,1,200.e3,1) 
line.SetLineColor(ROOT.kBlack) 
line.SetLineWidth(2) 
line.Draw("same")

legend = ROOT.TLegend(0.7,0.6,0.85,0.75) 
legend.AddEntry(mcHisto ,"MC") 
legend.AddEntry(dataHisto ,"Data") 
legend.SetLineWidth(0) 
legend.Draw("same")

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.06) 
latex.DrawText(0.7,0.83,"HASCO 2018") 
latex.SetTextSize(0.04) 
latex.DrawText(0.7,0.77,"Di-muon events")  

canvas.Print(plotFileName+"]")  


