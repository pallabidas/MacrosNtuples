from ROOT import TFile, TH1F, TH2, TCanvas
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
h_ptBalance = [] # Full list of histos
h_ptBalance_per_eta = [[] for _ in range(len(str_binetas))] # Nested lists for each eta region
for key in keys:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       h_ptBalance.append(histo2D.ProjectionY())
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
dir1 = 'control_plots_ptbalance_in_alpha_eta_bins'
os.makedirs(dir1, exist_ok = True)

index = 0
for e in range(len(jetetaBins)-1):
    str1 = '[' + str(round(jetetaBins[e],3)) + ',' + str(round(jetetaBins[e+1],3)) + ']'
    for a in range(len(alphaBins)-1):
        str2='[' + str(round(alphaBins[a],3)) + ',' + str(round(alphaBins[a+1],3)) +']'
        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
        h_ptBalance[index].SetTitle('p_{T} balance: #eta=' + str1 + ',' + '#alpha=' + str2)
        h_ptBalance[index].Draw()
        c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.png')
        #c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.pdf')
        index += 1

# Then for each rapidity region we take the mean (pt balance) and draw it as a function of alpha
dir2 = 'control_plots_jet_response_vs_alpha_in_etabins'
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
    str1='[' + str(round(jetetaBins[e],3)) + ',' + str(round(jetetaBins[e+1],3)) + ']'
    c = TCanvas(str1, str1, 1000, 1000)
    h_jetresponse[e].SetTitle('p_{T} balance: #eta=' + str1)
    h_jetresponse[e].Draw()
    c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + '.png')
    #c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + '.pdf')
