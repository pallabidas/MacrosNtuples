import ROOT
import os
import sys
import argparse
import numpy as np
colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kOrange, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kGray+1, ROOT.kCyan+2, ROOT.kYellow+2, ROOT.kOrange+2]
dirname = 'plotL1Run3_prov2/'

lumisection_in_seconds = 23.3


iszerobias = True
def canvas():
    c = ROOT.TCanvas("c_eff","c_eff",700,600)
    c.SetLeftMargin(0.15)
    c.SetRightMargin(0.15)
    return c


def eventcount_normalization(h_ref_rate_meas_vs_pu, rate_ref=5.7*2450, pu_ref=70, rate_zb=3e8/26659*2450, dataset='ZeroBias'):
    '''
    Derive a correction to convert event counts into rates, using counts for reference trigger (in the histo h_ref_rate_meas_vs_pu).
    For ZeroBias, the reference is just the L1_ZeroBias bit for which the rate is known and is rate_zb. 

    For HLTPhysics, things are more tricky as dead time can alter the measurement and is PU dependent. 
    The reference trigger here is L1_SingleMu22 whose rate is linear vs PU. 
    https://cmsoms.cern.ch/api/resources/rateplots/8456/L1_SingleMu22
    '''
    h_normalization_correction = ROOT.TH1F("h_normalization_correction_vs_pu","",100,0.5,100.5)
    for i in range(1, h_normalization_correction.GetNbinsX()):
        print(type(rate_ref),type(pu_ref),type(h_normalization_correction.GetBinCenter(i)))
        rate = rate_ref/pu_ref*h_normalization_correction.GetBinCenter(i)
        if dataset == 'ZeroBias':
            rate = rate_zb
        h_normalization_correction.SetBinContent(i,rate)
        
    h_normalization_correction.Divide(h_ref_rate_meas_vs_pu)

    return h_normalization_correction
#At PU70, unprescaled rate of L1_SingleMu22 is 5.7 Hz per bunch crossing. There are 2450 colliding bx in a typical fill


def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-i", "--input", dest="inputFile", help="Input file", type=str, default='')
    parser.add_argument("-d", "--dataset", dest="dataset", help="Dataset (HLTPhysics or ZeroBias)", type=str, default='')
    parser.add_argument("--histos", dest="histos", help="Name(s) of the histo(s)", nargs='+', type=str, default='')
    parser.add_argument("--href", dest="href", help="histo for ref", type=str, default='')
    parser.add_argument("--hlumis", dest="hlumis", help="histo for processed ls", type=str, default='')
    
    parser.add_argument("--ytitle", dest="ytitle", help="Y axis title", type=str, default='Number of entries')
    parser.add_argument("--ztitle", dest="ztitle", help="Z axis title", type=str, default='Number of entries')
    parser.add_argument("--lumi", dest="lumilabel", help="Integrated lumi and sqrt(s)", type=str, default='#sqrt{s} = 13.6 TeV, L_{int} #approx X fb^{-1}')
    parser.add_argument("--legend", dest="legendlabels", help="Legend labels", nargs='+', type=str, default='')
    parser.add_argument("--extralabel", dest="extralabel", help="Extra label", type=str, default='')
    parser.add_argument("--setlogx", dest="setlogx", help="Set log x", type=bool, default=False)
    parser.add_argument("--plotname", dest="plotname", help="Name of the plot", type=str, default='plot')
    parser.add_argument("--h2d", dest="h2d", help="2D histo (for profile etc)", nargs='+',type=str)
    parser.add_argument("--axisranges", dest="axisranges", help="Axis ranges [xmin, xmax, ymin, ymax, zmin, zmax]", nargs='+', type=float, default=[])
    parser.add_argument("--addnumtoden", dest="addnumtoden", help="Add numerator histo to denominator (because it only contains complementary events e.g. failing probes)",type=bool, default=False)
    parser.add_argument("--saveplot", dest="saveplot", help="Save plots or not",type=bool, default = False)
    parser.add_argument("--interactive", dest="interactive", help="Run in interactive mode (keep plot drawn)", type=bool, default=True)
    parser.add_argument("--suffix_files", dest="suffix_files", help="Input files suffix", nargs='+', type=str, default='')
        
    args = parser.parse_args()

    if args.dataset != 'ZeroBias' and args.dataset != 'HLTPhysics':
        raise Exception('Invalid dataset')
    
    if args.interactive == False:
        ROOT.gROOT.SetBatch(1)
        
    inputFile = ROOT.TFile(args.inputFile, "read")

    histos = []
    hlumis = inputFile.Get(args.hlumis)
    
    href = inputFile.Get(args.href)
    href.Divide(hlumis)
    href.Scale(1./lumisection_in_seconds)
    h_normalization_correction = eventcount_normalization(href, dataset=args.dataset)
    

    c = canvas()
    for ctr, i in enumerate(args.histos):
        print(i)
        histos.append(inputFile.Get(i).Clone())
        print(histos[-1].GetName(), histos[-1].GetEntries())
        
    legend = ROOT.TLegend(0.6,0.12,0.85,0.12+0.04*len(histos),"","mlNDC")
    legend.SetTextFont(42)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)

    for i, name in reversed(list(enumerate(args.legendlabels))):
        print(name)
        legend.AddEntry(histos[i], name,"lep")

    

        
    for ctr, i in reversed(list(enumerate(histos))):
        i.Divide(hlumis) 
        i.Scale(1./lumisection_in_seconds)
        i.Multiply(h_normalization_correction)
        i.SetMarkerStyle(20)
        i.SetLineColor(colors[ctr%len(colors)])
        #i.SetFillColor(colors[ctr%len(colors)])
        
        i.SetMarkerColor(colors[ctr%len(colors)])
        if ctr == len(histos):
            #i.Draw("hist")
            i.Draw("lep")
        else:
            #i.Draw("hist, same")
            i.Draw("lep, same")
    #histos[0].Draw()
    legend.Draw("same")
    c.Update()
    c.RedrawAxis()
    c.SaveAs("lol.pdf")
    if args.interactive == True:
        input()

if __name__ == '__main__':
    main()




    
