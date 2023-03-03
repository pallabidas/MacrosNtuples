import ROOT
import os
import sys
import argparse
import numpy as np
colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kOrange, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kGray+1, ROOT.kCyan+2, ROOT.kYellow+2, ROOT.kOrange+2]
dirname = 'plots/'

if not os.path.exists(dirname):
    os.makedirs(dirname)

def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-t", "--type", dest="type", help="Type of plots (hists, eff)", type=str, default='')
    parser.add_argument("-i", "--input", dest="inputFiles", help="Input file", nargs='+', type=str, default='')
    parser.add_argument("--histos", dest="histos", help="Name(s) of the histo(s)", nargs='+', type=str, default='')
    parser.add_argument("--den", dest="den", help="Name(s) of the histo denominator(s). There can be 1 or the same number as numerator histos ", nargs='+', type=str, default='')
    parser.add_argument("--num", dest="num", help="Name(s) of the histo numerator(s)", nargs='+', type=str, default='')
    parser.add_argument("--xtitle", dest="xtitle", help="X axis title", type=str, default='p_{T} (GeV)')
    parser.add_argument("--ytitle", dest="ytitle", help="Y axis title", type=str, default='Number of entries')
    parser.add_argument("--ztitle", dest="ztitle", help="Z axis title", type=str, default='Number of entries')
    parser.add_argument("--lumi", dest="lumilabel", help="Integrated lumi and sqrt(s)", type=str, default='#sqrt{s} = 13.6 TeV, L_{int} #approx X fb^{-1}')
    parser.add_argument("--legend", dest="legendlabels", help="Legend labels", nargs='+', type=str, default='')
    parser.add_argument("--extralabel", dest="extralabel", help="Extra label", type=str, default='')
    parser.add_argument("--setlogx", dest="setlogx", help="Set log x", type=bool, default=False)
    parser.add_argument("--setlogy", dest="setlogy", help="Set log y", type=bool, default=False)
    parser.add_argument("--plotname", dest="plotname", help="Name of the plot", type=str, default='plot')
    parser.add_argument("--h2d", dest="h2d", help="2D histo (for profile etc)", nargs='+',type=str)
    parser.add_argument("--axisranges", dest="axisranges", help="Axis ranges [xmin, xmax, ymin, ymax, zmin, zmax]", nargs='+', type=float, default=[])
    parser.add_argument("--addnumtoden", dest="addnumtoden", help="Add numerator histo to denominator (because it only contains complementary events e.g. failing probes)",type=bool, default=False)
    parser.add_argument("--saveplot", dest="saveplot", help="Save plots or not",type=bool, default = False)
    parser.add_argument("--interactive", dest="interactive", help="Run in interactive mode (keep plot drawn)", type=bool, default=False)
    parser.add_argument("--suffix_files", dest="suffix_files", help="Input files suffix", nargs='+', type=str, default='')
    parser.add_argument("--txtformat", dest="txtformat", help="SetPaintTextFormat option", type=str, default='2.2f')
    parser.add_argument("--normalized", dest="normalized", help="Draw normalized",type=bool, default = False)



    args = parser.parse_args()
    
    if args.interactive == False:
        ROOT.gROOT.SetBatch(1)

    ROOT.gStyle.SetPaintTextFormat(args.txtformat)
    
    inputFiles = []
    for i in args.inputFiles:
        inputFiles.append(ROOT.TFile(i,"read"))

    if args.type=='':
        histos = []
        for i in range(len(args.histos)):
            for inputFile in inputFiles:
                histos.append(inputFile.Get(args.histos[i]).Clone())
        drawplots(histos, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle=args.ytitle, ztitle=args.ztitle, lumilabel=args.lumilabel, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname=args.plotname, axisranges=args.axisranges, saveplot = args.saveplot, interactive=args.interactive, suffix_files = args.suffix_files, normalized = args.normalized)
        
    if args.type=='efficiency':
        h_dens = [] 
        h_nums = []
        for inputFile in inputFiles:
            print(inputFile.GetName())
            if len(args.den) !=1 and len(args.den)!=len(args.num):
                print("Numerator has {} histos while denominator has {}. Exiting.".format(len(h_nums),len(h_dens)))
                return 
            for i in range(len(args.num)):
                h_nums.append(inputFile.Get(args.num[i]).Clone())
                if len(args.den)==1:
                    h_dens.append(inputFile.Get(args.den[0]).Clone())
                else:
                    h_dens.append(inputFile.Get(args.den[i]).Clone())
                h_nums[i].SetName(h_nums[i].GetName()+"_{}".format(i))
                h_dens[i].SetName(h_dens[i].GetName()+"_{}".format(i))
        effs = compute_eff(h_dens, h_nums, args.addnumtoden)
        drawplots(effs, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle=args.ytitle, ztitle=args.ztitle, lumilabel=args.lumilabel, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname=args.plotname, axisranges=args.axisranges, saveplot = args.saveplot, interactive=args.interactive, suffix_files = args.suffix_files)
            
    if args.type=='profilex_fromh2':
        h2ds = []
        for i in args.h2d:
            h2ds.append(inputFiles[0].Get(i).Clone())
        profiles = compute_profilex(h2ds)
        drawplots(profiles, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle=args.ytitle, ztitle=args.ztitle, lumilabel=args.lumilabel, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname=args.plotname, axisranges=args.axisranges, saveplot = args.saveplot, interactive=args.interactive)

    if args.type=='resolvsx':
        h2ds = []
        newbinsx = [30.+i*2 for i in range(0,10) ] + [50.+i*5 for i in range(0,10) ] + [100., 110., 120., 130., 150., 200., 300.]
        for ctr, inputFile in enumerate(inputFiles):
            for i in range(len(args.h2d)):
                #hprov=inputFile.Get(args.h2d[i]).Clone()
                hprov=rebinth2d(inputFile.Get(args.h2d[i]).Clone(), newbinsx)
                h2ds.append(hprov)
                h2ds[-1].SetName(h2ds[-1].GetName()+"_{}".format(i)+"_{}".format(ctr))
                print('hname: ',h2ds[-1].GetName())

        hresponse, hresol = compute_ResolutionvsX(h2ds)
        drawplots(hresponse, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle='#mu'+args.ytitle, ztitle=args.ztitle, lumilabel=args.lumilabel, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname='mu_'+args.plotname, axisranges=args.axisranges, saveplot = args.saveplot, interactive=args.interactive, suffix_files = args.suffix_files)
        axisranges = args.axisranges
        axisranges[2] = 0
        axisranges[3] = 0.5
        drawplots(hresol, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle='#sigma_{scale corr.}'+args.ytitle, ztitle=args.ztitle, lumilabel=args.lumilabel, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname='resol_'+args.plotname, axisranges=axisranges, saveplot = args.saveplot, interactive=args.interactive)

        
        

def canvas():
    c = ROOT.TCanvas("c_eff","c_eff",700,600)
    c.SetLeftMargin(0.15)
    c.SetRightMargin(0.15)
    return c


def drawplots(objs, legendlabels, xtitle='', ytitle='', ztitle='', lumilabel='', extralabel='', setlogx=False, setlogy=False, plotname='plot', axisranges=[], saveplot=False, interactive=False, suffix_files = [], normalized=False):
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    #ROOT.gStyle.SetPaintTextFormat("2.2f")
    ROOT.gStyle.SetPalette(1)
    c = canvas()

    labelsize = len(legendlabels)
    for suffix in suffix_files:
        for j in range(labelsize):
            legendlabels.append(legendlabels[j] + suffix)

    if len(suffix_files)>0:
        del legendlabels[0:labelsize]
    
    if len(legendlabels) != len(objs):
        print("Some histos are missing a legend. ")
        print("len(legendlabels) != len(objs): ", len(legendlabels),"!=", len(objs))
        legendlabels=[]
        for i in range(len(objs)):
            legendlabels.append('')
            

    
    legend = ROOT.TLegend(0.6,0.32,0.85,0.32+0.04*len(objs),"","mlNDC")
    if plotname.find('resol')>=0:
        legend.SetY1(0.5)
        legend.SetY2(0.5+0.04*len(objs))
        
    legend.SetTextFont(42)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
        
    objs[0].SetTitle(";{};{};{}".format(xtitle,ytitle,ztitle))
    objs[0].SetLineColor(colors[0])
    if objs[0].GetDimension () == 1:
        if normalized:
            objs[0].DrawNormalized()
        else:
            objs[0].Draw()

    elif type(objs[0])==ROOT.TEfficiency and objs[0].GetDimension () == 2:
        objs[0].Draw("TEXT ZCOL")
        objs[0].SetName(plotname)
        objs[0].SaveAs(dirname+'/'+plotname+'.root')

    else:
        if normalized:
            objs[0].DrawNormalized("ZCOL")
        else:
            objs[0].Draw("ZCOL")



    #if setlogx:
    c.SetLogx(setlogx)
    #if setlogy:
    c.SetLogy(setlogy)
    c.Update()
    drawnobject = None
    if type(objs[0])==ROOT.TEfficiency and objs[0].GetDimension () == 1:
        drawnobject = objs[0].GetPaintedGraph()
    elif type(objs[0])==ROOT.TEfficiency and objs[0].GetDimension () == 2:
        drawnobject = objs[0].GetPaintedHistogram()
        objs[0].SetMarkerSize(1.2)
        
    else:
        drawnobject = objs[0]

    drawnobject.GetXaxis().SetMoreLogLabels()
    drawnobject.GetXaxis().SetNoExponent()
    drawnobject.GetYaxis().SetMoreLogLabels()
    drawnobject.GetYaxis().SetNoExponent()
    drawnobject.GetXaxis().SetTitleSize(0.04)
    drawnobject.GetYaxis().SetTitleSize(0.04)
    if objs[0].GetDimension() >=2:
        drawnobject.GetZaxis().SetTitleSize(0.04)
    if len(axisranges)>=2:
        drawnobject.GetXaxis().SetRangeUser(axisranges[0],axisranges[1])
    if len(axisranges)>=4:
        drawnobject.GetYaxis().SetRangeUser(axisranges[2],axisranges[3])
    if len(axisranges)>=6:
        drawnobject.GetZaxis().SetRangeUser(axisranges[4],axisranges[5])
    if len(axisranges)<4 and objs[0].GetDimension() == 1 and type(objs[0]) == ROOT.TEfficiency : 
        drawnobject.GetYaxis().SetRangeUser(0., 1.3) 
        
    print(type(objs))

    #2D efficiency 
    #Special treatment needed because the default TH2F is unable to show asymmetric error bars 
    drawnobject_errup = None
    drawnobject_errlow = None
    if type(objs[0]) == ROOT.TEfficiency and objs[0].GetDimension () == 2:
        
        drawnobject_errup = drawnobject.Clone()
        drawnobject_errlow = drawnobject.Clone()
        drawnobject.SetBarOffset(+0.1)
        for i in range(1, drawnobject_errup.GetNbinsX()+1):
            for j in range(1, drawnobject_errup.GetNbinsY()+1):
                ibin = drawnobject.GetBin(i,j)
                if objs[0].GetEfficiencyErrorUp(ibin) !=1 and objs[0].GetTotalHistogram().GetBinContent(ibin) !=0:
                    drawnobject_errup.SetBinContent(i, j, max(1e-7, objs[0].GetEfficiencyErrorUp(ibin)))
                    print(objs[0].GetEfficiencyErrorUp(ibin))
                else:
                    drawnobject_errup.SetBinContent(i, j, 0)

                if objs[0].GetTotalHistogram().GetBinContent(ibin) !=0:
                    drawnobject_errlow.SetBinContent(i, j, -objs[0].GetEfficiencyErrorLow(ibin))
                    print(-objs[0].GetEfficiencyErrorLow(ibin))
                else:
                    drawnobject_errlow.SetBinContent(i, j, 0)
        drawnobject_errup.SetBarOffset(-0.25)
        drawnobject_errup.SetMarkerSize(0.8)
        drawnobject_errup.Draw("TEXT SAME")
        drawnobject_errlow.GetZaxis().SetRangeUser(-1,1)
        drawnobject_errup.GetZaxis().SetRangeUser(-1,1)
        drawnobject_errlow.SetMarkerSize(0.8)
        drawnobject_errlow.SetBarOffset(-0.1)
        drawnobject_errlow.Draw("TEXT SAME")

    c.Update()
    
    for i, h in enumerate(objs):
        objs[i].SetLineColor(colors[i])
        if legendlabels[i] != '':
            legend.AddEntry(h,legendlabels[i],"lep")
        if i>0:
            if normalized:
                objs[i].DrawNormalized("sames")
            else:
                objs[i].Draw("sames")


            
    #Next lines for fitting
    ROOT.gStyle.SetFitFormat("3.3f")
    ROOT.gStyle.SetOptFit(11)
    fitfn = []
    for i in range(len(objs)):
        fitfn.append(ROOT.TF1("erf_{}"+format(i),"0.5*[0]*(TMath::Erf((x-[1])/[2])+1)", 170, 400))
        fitfn[-1].SetParLimits(0,0.9,1.1)
        fitfn[-1].SetParName(0,"#epsilon_{#infty}")
        fitfn[-1].SetParName(1,"#mu")
        fitfn[-1].SetParName(2,"#sigma")
        fitfn[-1].SetParLimits(1,50,200)
        fitfn[-1].SetParLimits(2,0.0001,100)
        fitfn[-1].SetLineColor(colors[i])
    stats = []
    gphtofit = []
    for i, h in enumerate(objs):
        if type(objs[i])==ROOT.TEfficiency and objs[i].GetDimension () == 1: 
            #gphtofit = objs[i].GetPaintedGraph()
            gphtofit.append(objs[i].GetPaintedGraph())
            if gphtofit[i] == 0:
                continue

            '''
            h.Fit(fitfn[i],"R")
            fitfn[i].Draw("same")
            c.Update()
            stats.append(gphtofit[i].FindObject("stats"))
            
            stats[i].Draw("same")
            stats[i].SetTextColor(colors[i])
            stats[i].SetFillStyle(0)
            stats[i].SetX1NDC(0.6)
            stats[i].SetX2NDC(0.85)
            stats[i].SetY1NDC(0.25+i*0.2)
            stats[i].SetY2NDC(0.45+i*0.2)
            '''
            c.Update()

            
    label_cms = ROOT.TLatex()
    label_cms.SetTextSize(0.05)
    label_cms.DrawLatexNDC(0.15, 0.92, "#bf{CMS} #it{Internal}")
    label_lumi = ROOT.TLatex()
    label_lumi.SetTextSize(0.04)
    label_lumi.SetTextAlign(31)
#    label_lumi.DrawLatexNDC(0.5, 0.92, "#sqrt{s} = 13.6 TeV, L_{int} #approx 9 fb^{-1}")
    label_lumi.DrawLatexNDC(0.85, 0.92, lumilabel)

    #label_extra = ROOT.TPaveLabel(0.17,0.75,0.9,0.9,"#color[2]{"+extralabel+"}","brNDC")
    label_extra = ROOT.TPaveLabel(0.2,0.75,0.5,0.92,"#color[2]{"+extralabel+"}","brNDC")

    label_extra.SetTextFont(43)
    label_extra.SetTextAlign(12)
    label_extra.SetTextSize(30)
    label_extra.SetFillStyle(0)
    label_extra.SetBorderSize(0)
    label_extra.Draw()

    
    legend.Draw()
    if interactive:
        input()
    if saveplot: 
        c.SaveAs(dirname+'/'+plotname+'.png')
        c.SaveAs(dirname+'/'+plotname+'.pdf')
        

def compute_eff(hdens, hnums, addnumtoden):
    effs = []
    for i in range(len(hnums)):
        if addnumtoden:
            hdens[i].Add(hnums[i])
        hnums[i].Sumw2()
        hdens[i].Sumw2()
        if hnums[i].GetNbinsX()>=500:
            hdens[i].Rebin(5)
            hnums[i].Rebin(5)
        
        eff = ROOT.TEfficiency(hnums[i], hdens[i])
        eff.SetFillStyle(0)
        eff.SetLineColor(colors[i])
        eff.SetMarkerStyle(20)
        eff.SetMarkerSize(0.5)
        eff.SetMarkerColor(colors[i])
        effs.append(eff)

    return effs

def setstyle(h, i):
    h.SetFillStyle(0)
    h.SetLineColor(colors[i])
    h.SetMarkerStyle(20)
    h.SetMarkerSize(0.5)
    h.SetMarkerColor(colors[i])
    return h


def compute_profilex(h2d):
    profiles = []
    for i, h in enumerate(h2d):
        profile = h.ProfileX().Clone()
        profile.SetFillStyle(0)
        profile.SetLineColor(colors[i])
        profile.SetMarkerStyle(20)
        profile.SetMarkerSize(0.5)
        profile.SetMarkerColor(colors[i])
        profiles.append(profile)
    
    return profiles

def compute_ResolutionvsX(h2d):
    histos_response, histos_resol = [], []
    for ctr, h in enumerate(h2d):
        h_responsevsX = h.ProjectionX().Clone()
        h_resolvsX = h.ProjectionX().Clone()

        setstyle(h_responsevsX, ctr)
        setstyle(h_resolvsX, ctr)
        for i in range(h.GetNbinsX()+1):
            proj = h.ProjectionY("py",i,i).Clone()
            print("mean ", proj.GetMean())
            f_gaus = ROOT.TF1("f_gaus","gaus")
            proj.Fit(f_gaus,"Q")
            if f_gaus.GetParameter(1) >0 and f_gaus.GetParError(2)/f_gaus.GetParameter(1)<10.03:
                h_responsevsX.SetBinContent(i,f_gaus.GetParameter(1))
                h_responsevsX.SetBinError(i,f_gaus.GetParError(1))
                h_resolvsX.SetBinContent(i,f_gaus.GetParameter(2)/f_gaus.GetParameter(1))
                h_resolvsX.SetBinError(i,f_gaus.GetParError(2)/f_gaus.GetParameter(1))
            else:
                h_responsevsX.SetBinContent(i,0)
                h_responsevsX.SetBinError(i,0)
                h_resolvsX.SetBinContent(i,0)
                h_resolvsX.SetBinError(i,0)

        histos_resol.append(h_resolvsX)
        histos_response.append(h_responsevsX)
    return histos_response, histos_resol




def rebinth2d(h2d, newbinsx):
    newbinsx_np = np.array(newbinsx)
    newbinsx_np_unique = np.unique(newbinsx_np)
    newh2d = ROOT.TH2F(h2d.GetName()+"_rebin", "", newbinsx_np_unique.size-1, newbinsx_np_unique, h2d.GetNbinsY(), h2d.GetYaxis().GetXmin(), h2d.GetYaxis().GetXmax())
    for i in range(h2d.GetNbinsX()+1):
        for j in range(h2d.GetNbinsY()+1):
            val = h2d.GetBinContent(i, j)
            xbincenter = h2d.GetXaxis().GetBinCenter(i)
            ybincenter = h2d.GetYaxis().GetBinCenter(j)
            ibin = newh2d.FindBin(xbincenter, ybincenter)
            newh2d.SetBinContent(ibin, newh2d.GetBinContent(ibin)+val)
            #if h2d.GetXaxis().GetBinLowEdge(i) 
            #val += 
    return newh2d

    

def fittoerf(gph, fn):
    gphtofit = gph.GetPaintedGraph()
    #    print("in fit, gph has ", gphtofit.GetN())
    gphtofit.Fit(fn)




if __name__ == '__main__':
    main()




    
