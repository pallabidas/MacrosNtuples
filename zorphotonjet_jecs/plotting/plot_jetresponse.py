from ROOT import TFile, TH1F, TH2, TCanvas, gStyle, gPad
from ROOT import TAttMarker, TColor
from ROOT import kBlack, kBlue, kRed
from array import array
import os

# Input file
infile = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/EGamma/RunC/Test/All.root')

# Eta bins as floats and as strings
jetetaBins = [0.0, 1.3, 2.5, 3.0, 3.5, 4.0, 5.0]
str_binetas = []
for e in range(len(jetetaBins)-1):
    str_binetas.append("eta{}to{}".format(jetetaBins[e], jetetaBins[e+1]).replace(".","p"))
#print('Eta bins as strings: ',str_binetas)

# Alpha bins as floats and as strings
alphaBins = array('f', [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00])

nalphaBins = len(alphaBins)-1
str_binalphas = []
for a in range(len(alphaBins)-1):
    str_binalphas.append("alpha{}to{}".format(round(alphaBins[a],3), round(alphaBins[a+1],3)).replace(".","p"))
#print('Alpha bins as strings: ',str_binalphas)

# Get the 2D histograms with the pt balance and create the Y projections
keys = infile.GetListOfKeys()
h_ptBalance = [] # Full list of histos for each eta and alpha bin
h_ptBalance_vs_refpt = [] # Full list of histos for each eta and alpha bin
h_ptBalance_per_eta = [[] for _ in range(len(str_binetas))] # Nested lists for each eta region
for key in keys:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       h_ptBalance.append(histo2D.ProjectionY())
       h_ptBalance_vs_refpt.append(histo2D.ProfileX())
       name = key.GetName()
       for e, str_bineta in enumerate(str_binetas):
           if str_bineta in name:
              h_ptBalance_per_eta[e].append(histo2D.ProjectionY())

# Print the lists for checks
#print('Full list of histos: ')
#for h in range(len(h_ptBalance)):
#    print(h_ptBalance[h])
#print('Sublists: ')
#for l in range(len(h_ptBalance_per_eta)):
#    print("List #", l ,'for eta =',str_binetas[l])
#    for e in range(len(h_ptBalance_per_eta[l])):
#        print(h_ptBalance_per_eta[l][e])
#    print()

# First create canvases with all the pt balance plots for all eta and alpha bins
dir0 = 'jet_response'
os.makedirs(dir0, exist_ok = True)

index = 0
for e in range(len(jetetaBins)-1):
    str1 = '[' + str(round(jetetaBins[e],3)) + ',' + str(round(jetetaBins[e+1],3)) + ')'
    for a in range(len(alphaBins)-1):
        str2='[' + str(round(alphaBins[a],3)) + ',' + str(round(alphaBins[a+1],3)) +')'
        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
        h_ptBalance[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2)
        h_ptBalance[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma}')
        h_ptBalance[index].GetXaxis().SetTitleOffset(1.2)
        h_ptBalance[index].GetYaxis().SetTitle('Events')
        h_ptBalance[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance[index].GetYaxis().SetTitleOffset(1.5)
        h_ptBalance[index].Draw()
        c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.png')
        #c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.pdf')
        index += 1

# Then create canvases with all the pt balance plots vs pt_ref for all eta and alpha bins
dir1 = 'jet_response_vs_refpt'
os.makedirs(dir1, exist_ok = True)

index = 0
for e in range(len(jetetaBins)-1):
    str1 = '[' + str(round(jetetaBins[e],3)) + ',' + str(round(jetetaBins[e+1],3)) + ')'
    for a in range(len(alphaBins)-1):
        str2='[' + str(round(alphaBins[a],3)) + ',' + str(round(alphaBins[a+1],3)) +')'
        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
        gStyle.SetOptStat(0)
        gPad.SetLogx()
        h_ptBalance_vs_refpt[index].GetXaxis().SetMoreLogLabels()
        h_ptBalance_vs_refpt[index].GetXaxis().SetNoExponent()
        h_ptBalance_vs_refpt[index].SetMaximum(1.15)
        h_ptBalance_vs_refpt[index].SetMinimum(0.75)
        h_ptBalance_vs_refpt[index].SetMarkerStyle(8)
        h_ptBalance_vs_refpt[index].SetMarkerSize(1.4)
        h_ptBalance_vs_refpt[index].SetMarkerColor(kBlue+1)
        h_ptBalance_vs_refpt[index].SetLineColor(kBlue+1)
        h_ptBalance_vs_refpt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2)
        h_ptBalance_vs_refpt[index].GetXaxis().SetTitle('p_{T}^{#gamma}')
        h_ptBalance_vs_refpt[index].GetXaxis().SetTitleOffset(1.3)
        h_ptBalance_vs_refpt[index].GetYaxis().SetTitle('p_{T} balance')
        h_ptBalance_vs_refpt[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance_vs_refpt[index].GetYaxis().SetTitleOffset(1.4)
        h_ptBalance_vs_refpt[index].Draw()
        c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.png')
        #c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.pdf')
        index += 1

# Then for each rapidity region we take the mean (pt balance) and draw it as a function of alpha
dir2 = 'jet_response_vs_alpha'
os.makedirs(dir2, exist_ok = True)

h_means = [[]for _ in range(len(str_binetas))]  # List with all the mean values
h_errors = [[]for _ in range(len(str_binetas))] # List with all the mean value errors
for e in range(len(str_binetas)):
    for b in range(len(h_ptBalance_per_eta[e])):
        h_means[e].append(h_ptBalance_per_eta[e][b].GetMean())
        h_errors[e].append(h_ptBalance_per_eta[e][b].GetMeanError())
#print('Lists with mean values (each list is an eta region): ',h_means)
#print('Lists with errors in the mean values ((each list is an eta region):',h_errors)

# Jet response vs alpha (for each eta region) histograms
h_jetresponse = []
for e in range(len(str_binetas)):
    h = TH1F('jet_response_' + str_binetas[e], 'jet_response_' + str_binetas[e], nalphaBins, alphaBins)
    for a in range(nalphaBins):
         h.SetBinContent(a+1, h_means[e][a])
         h.SetBinError(a+1, h_errors[e][a])
    h_jetresponse.append(h)

for e in range(len(jetetaBins)-1):
    str1='[' + str(round(jetetaBins[e],3)) + ',' + str(round(jetetaBins[e+1],3)) + ')'
    c = TCanvas(str1, str1, 1000, 1000)
    gStyle.SetOptStat(0)
    h_jetresponse[e].SetMarkerStyle(8)
    h_jetresponse[e].SetMarkerSize(1.4)
    h_jetresponse[e].SetMarkerColor(kBlue+1)
    h_jetresponse[e].SetLineColor(kBlue+1)
    h_jetresponse[e].SetTitle('p_{T} balance: #eta=' + str1)
    h_jetresponse[e].GetXaxis().SetTitle('#alpha')
    h_jetresponse[e].GetXaxis().SetTitleSize(0.045)
    h_jetresponse[e].GetXaxis().SetTitleOffset(1.0)
    h_jetresponse[e].GetYaxis().SetTitle('p_{T} balance')
    h_jetresponse[e].GetYaxis().SetTitleSize(0.045)
    h_jetresponse[e].GetYaxis().SetLabelSize(0.035)
    h_jetresponse[e].GetYaxis().SetTitleOffset(1.0)
    h_jetresponse[e].Draw()
    c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + '.png')
    #c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + '.pdf')
