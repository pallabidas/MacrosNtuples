from ROOT import TFile, TH1F, TH2, TCanvas, gDirectory, gStyle, gPad
from ROOT import TAttMarker, TColor
from ROOT import kBlack, kBlue, kRed
from array import array
import os
import sys

sys.path.insert(1, '../') # for importing the binning
from binning import *

# Input file : TODO Make it an argument
infile = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/EGamma/RunC/Test/All.root')

# Eta bins as strings
str_binetas = []
for e in range(len(jetetaBins)-1):
    str_binetas.append("eta{}to{}".format(jetetaBins[e], jetetaBins[e+1]).replace(".","p"))
#print('Eta bins as strings: ',str_binetas)

# pT bins as strings
nptBins = len(jetptBins)-1
str_binpts = []
for p in range(len(jetptBins)-1):
    str_binpts.append("pt{}to{}".format(int(jetptBins[p]), int(jetptBins[p+1])))
#print('Pt bins as strings: ',str_binpts)

# Alpha bins as floats and as strings (Define also here as array for histogram booking later)
alphaBins = array('f', [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00])

nalphaBins = len(alphaBins)-1
str_binalphas = []
for a in range(len(alphaBins)-1):
    str_binalphas.append("alpha{}to{}".format("{:.2f}".format(alphaBins[a]), "{:.2f}".format(alphaBins[a+1])).replace(".","p"))
#print('Alpha bins as strings: ',str_binalphas)

# Get the 2D histograms with the pt balance and create the Y projections
keys = infile.GetListOfKeys()
h_ptBalance = [] # Full list of histos for each eta, alpha and pt bin
h_ptBalance_vs_refpt = [] # Full list of histos for each eta, alpha and pt bin

# Create a dictionary of lists for each pt and eta region
str_binetas_pts = []
for e in str_binetas:
    for p in str_binpts:
       str_binetas_pts.append(e + p)
#print(str_binetas_pts)

h_ptBalance_per_eta_per_pt = dict([(k, []) for k in str_binetas_pts])

for key in keys:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       h_ptBalance.append(histo2D.ProjectionY())
       h_ptBalance_vs_refpt.append(histo2D.ProfileX())
       name = key.GetName() 
       for e in str_binetas:
           if e in name:
              for p in str_binpts:
                  if p in name:
                     h_ptBalance_per_eta_per_pt[e+p].append(histo2D.ProjectionY())

# Print the lists for checks
#print('Full list of histos: ')
#for h in range(len(h_ptBalance)):
#    print(h_ptBalance[h])
#for k, h in h_ptBalance_per_eta_per_pt.items():
#    print(f'Key: {k}')
#    for name in h:
#        print(f'Histogram: {name}')

# First create canvases with all the pt balance plots for all eta and alpha bins
#dir0 = 'jet_response'
#os.makedirs(dir0, exist_ok = True)
#
#index = 0
#for e in range(len(jetetaBins)-1):
#    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
#    for a in range(len(alphaBins)-1):
#        str2='[' + str("{:.2f}".format(alphaBins[a])) + ',' + str("{:.2f}".format(alphaBins[a+1])) +')'
#        for p in range(len(jetptBins)-1):
#            str3 = '[' + str(jetptBins[p]) + ',' + str(jetptBins[p+1]) + ')'
#            c = TCanvas(str1 + ',' + str2 + ',' + str3, str1 + ',' + str2 + ',' + str3, 1000, 1000)
#            h_ptBalance[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2 + ', ' + 'p_{T}^{#gamma}=' + str3)
#            h_ptBalance[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma}')
#            h_ptBalance[index].GetXaxis().SetTitleOffset(1.2)
#            h_ptBalance[index].GetYaxis().SetTitle('Events')
#            h_ptBalance[index].GetYaxis().SetLabelSize(0.03)
#            h_ptBalance[index].GetYaxis().SetTitleOffset(1.5)
#            h_ptBalance[index].Draw()
#            c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p] + '.png')
#            #c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p] + '.pdf')
#            index += 1
#
# Then create canvases with all the pt balance plots vs pt_ref for all eta and alpha bins
#dir1 = 'jet_response_vs_refpt'
#os.makedirs(dir1, exist_ok = True)
#
#index = 0
#for e in range(len(jetetaBins)-1):
#    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
#    for a in range(len(alphaBins)-1):
#        str2='[' + str("{:.2f}".format(alphaBins[a])) + ',' + str("{:.2f}".format(alphaBins[a+1])) +')'
#        #print('Adding histograms to: ', h_ptBalance_vs_refpt[index].GetName())
#        # Here we add all the different pt histograms such that we have one histogram per eta and alpha bin
#        for p in range(len(jetptBins)-2):
#            h_ptBalance_vs_refpt[index].Add(h_ptBalance_vs_refpt[index+p+1])
#            #print(' adding: ', h_ptBalance_vs_refpt[index+p+1].GetName())
#        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
#        gStyle.SetOptStat(0)
#        gPad.SetLogx()
#        h_ptBalance_vs_refpt[index].GetXaxis().SetMoreLogLabels()
#        h_ptBalance_vs_refpt[index].GetXaxis().SetNoExponent()
#        h_ptBalance_vs_refpt[index].SetMaximum(1.15)
#        h_ptBalance_vs_refpt[index].SetMinimum(0.75)
#        h_ptBalance_vs_refpt[index].SetMarkerStyle(8)
#        h_ptBalance_vs_refpt[index].SetMarkerSize(1.4)
#        h_ptBalance_vs_refpt[index].SetMarkerColor(kBlue+1)
#        h_ptBalance_vs_refpt[index].SetLineColor(kBlue+1)
#        h_ptBalance_vs_refpt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2)
#        h_ptBalance_vs_refpt[index].GetXaxis().SetTitle('p_{T}^{#gamma}')
#        h_ptBalance_vs_refpt[index].GetXaxis().SetTitleOffset(1.3)
#        h_ptBalance_vs_refpt[index].GetYaxis().SetTitle('p_{T} balance')
#        h_ptBalance_vs_refpt[index].GetYaxis().SetLabelSize(0.03)
#        h_ptBalance_vs_refpt[index].GetYaxis().SetTitleOffset(1.4)
#        h_ptBalance_vs_refpt[index].Draw()
#        c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.png')
##        #c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.pdf')
#        index += nptBins

# Then for each eta and each pt bin we take the mean (pt balance) and draw it as a function of alpha
#dir2 = 'jet_response_vs_alpha'
#os.makedirs(dir2, exist_ok = True)

h_means = {}  #Dictionary with the mean values
h_errors = {} #Dictionary with the mean value errors

for k, h in h_ptBalance_per_eta_per_pt.items():
    mean_values = []
    mean_errors = [] 
    for histo in h:
        mean_values.append(histo.GetMean())     
        mean_errors.append(histo.GetMeanError())     
    h_means[k] = mean_values
    h_errors[k] = mean_errors

#    for b in range(len(h_ptBalance_per_eta[e])):
#        h_means[e].append(h_ptBalance_per_eta[e][b].GetMean())
#        h_errors[e].append(h_ptBalance_per_eta[e][b].GetMeanError())
#print('Lists with mean values (each list is an eta region): ',h_means)
#print('Lists with errors in the mean values ((each list is an eta region):',h_errors)



# Jet response vs alpha (for each eta region) and each pt bin
#h_jetresponse = []
#for e in range(len(str_binetas)):
#    for p in range(len(str_binpts)):
#        h = TH1F('jet_response_' + str_binetas[e] + str_binpts[p], 'jet_response_' + str_binetas[e] + str_binpts[p], nalphaBins, alphaBins)
#        for a in range(nalphaBins):
#            h.SetBinContent(a+1, h_means[e][a])
#            h.SetBinError(a+1, h_errors[e][a])
#        h_jetresponse.append(h)



#for e in range(len(jetetaBins)-1):
#    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
#    c = TCanvas(str1, str1, 1000, 1000)
#    gStyle.SetOptStat(0)
#    h_jetresponse[e].SetMarkerStyle(8)
#    h_jetresponse[e].SetMarkerSize(1.4)
#    h_jetresponse[e].SetMarkerColor(kBlue+1)
#    h_jetresponse[e].SetLineColor(kBlue+1)
#    h_jetresponse[e].SetTitle('p_{T} balance: #eta=' + str1)
#    h_jetresponse[e].GetXaxis().SetTitle('#alpha')
#    h_jetresponse[e].GetXaxis().SetTitleSize(0.045)
#    h_jetresponse[e].GetXaxis().SetTitleOffset(1.0)
#    h_jetresponse[e].GetYaxis().SetTitle('p_{T} balance')
#    h_jetresponse[e].GetYaxis().SetTitleSize(0.045)
#    h_jetresponse[e].GetYaxis().SetLabelSize(0.035)
#    h_jetresponse[e].GetYaxis().SetTitleOffset(1.0)
#    h_jetresponse[e].Draw()
#    c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + '.png')
#    #c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + '.pdf')
