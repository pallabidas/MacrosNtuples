import ROOT
import os
import sys
import argparse
import numpy as np
colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kOrange, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kGray+1, ROOT.kCyan+2, ROOT.kYellow+2, ROOT.kOrange+2]
dirname = 'plotL1Run3_prov2/'

lumisection_in_seconds = 23.3
prescale = 450.
rate_meas = 5.7*2450.
rate_zb = 3e8/26659*2450
iszerobias = True
def canvas():
    c = ROOT.TCanvas("c_eff","c_eff",700,600)
    c.SetLeftMargin(0.15)
    c.SetRightMargin(0.15)
    return c


def deadtime_correction(h_ref_rate_meas_vs_pu, rate_ref=5.7*2450, pu_ref=70):
    '''
    Define a PU dependent correction factor to account for dead time.
    A good reference is SingleMu22 which is quite linear with PU.
    https://cmsoms.cern.ch/api/resources/rateplots/8456/L1_SingleMu22
    '''
    h_deadtime_correction = ROOT.TH1F("h_deadtime_correction_vs_pu","",100,0.5,100.5)
    for i in range(1, h_deadtime_correction.GetNbinsX()):
        rate = rate_meas/pu_ref*h_deadtime_correction.GetBinCenter(i)
        if iszerobias:
            rate = rate_zb
        h_deadtime_correction.SetBinContent(i,rate)
        
    h_deadtime_correction.Divide(h_ref_rate_meas_vs_pu)

    return h_deadtime_correction
#At PU70, unprescaled rate of L1_SingleMu22 is 5.7 Hz per bunch crossing. There are 2450 colliding bx in a typical fill


def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-i", "--input", dest="inputFile", help="Input file", type=str, default='')
    
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
    
    if args.interactive == False:
        ROOT.gROOT.SetBatch(1)
        
    inputFile = ROOT.TFile(args.inputFile, "read")

    histos = []
    hlumis = inputFile.Get(args.hlumis)
    
    href = inputFile.Get(args.href)
    href.Divide(hlumis)
    href.Scale(1./lumisection_in_seconds)
    h_deadtime_correction = deadtime_correction(href)
    

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
        i.Multiply(h_deadtime_correction)
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




    
