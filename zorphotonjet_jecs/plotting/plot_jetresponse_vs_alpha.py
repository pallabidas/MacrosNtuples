from ROOT import TFile, TH1F, TH2, TCanvas
from array import array
import os

# Input file
infile = TFile('All.root')

# Eta bins as floats and as strings
jetetaBins = [0.0, 1.3, 2.5, 3.0, 3.5, 4.0, 5.0]
str_binetas = []
for e in range(len(jetetaBins)-1):
    str_binetas.append("eta{}to{}".format(jetetaBins[e], jetetaBins[e+1]).replace(".","p"))

# Alpha bins
alphaBins = array('f', [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50, 1.00])
nalphaBins = len(alphaBins)-1
str_binalphas = []
for a in range(len(alphaBins)-1):
    str_binalphas.append("alpha{}to{}".format(round(alphaBins[a],3), round(alphaBins[a+1],3)).replace(".","p"))

print(str_binalphas)
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

# Print the list for checks
#for l in range(len(h_ptBalance_per_eta)):
#    print("List #", l ,'for eta =',str_binetas[l])
#    for e in range(len(h_ptBalance_per_eta[l])):
#       print(h_ptBalance_per_eta[l][e])
#    print()
    
# First create canvases with all the pt balance plots for all eta and alpha bins
dir1 = 'control_plots_ptbalance_in_alpha_eta_bins'
os.makedirs(dir1, exist_ok = True)

index = 0
for a in range(len(alphaBins)-1):
    for e in range(len(jetetaBins)-1):
       c = TCanvas('alpha=['+str(alphaBins[a])+','+str(alphaBins[a+1])+']' + ' , ' + 'eta=['+str(jetetaBins[e])+','+str(jetetaBins[e+1])+']','Canvas', 1000, 1000 )
       h_ptBalance[index].SetTitle('p_{T} balance: #alpha=['+str(alphaBins[a])+','+str(alphaBins[a+1])+'], '+' #eta=['+str(jetetaBins[e])+','+str(jetetaBins[e+1])+']')
       h_ptBalance[index].Draw()
       c.SaveAs(dir1+'/ptBalance_'+str_binalphas[a] + '_' + str_binetas[e]+'.pdf')
       index += 1

 Then for each rapidity region we take the mean (pt balance) and draw it as a function of alpha
dir2 = 'control_plots_jet_response_vs_alpha_in_etabins'
os.makedirs(dir2, exist_ok = True)

h_means = []
h_errors = []
for e in range(len(str_binetas)):
    for l in range(len(h_ptBalance_per_eta[e])):    
        h_means[e].append(h_ptBalance_per_eta[l][e].GetMean())
        h_errors[e].append(h_ptBalance_per_eta[l][e].GetMeanError())
    
h_jetresponse = []
for e in range(len(str_binetas)):
    h = TH1F('jet_response_'+str_binetas[e],'jet_response_'+str_binetas[e], nalphaBins, alphaBins)
    for b in range(h.GetNbinsX()):
       ...
    h_jetresponse.append(h)
