# make_mu_plots.py, a program to draw the L1Studies plots obtained from the histograms extracted from NanoAOD

import yaml
import drawplots
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-d", "--dir", dest="dir", help="The directory to read the inputs files from and draw the plots to", type=str, default='./')
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default='../l1macros/full_ZToMuMu.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')
    parser.add_argument("--plot_nvtx", dest="plot_nvtx", help="Whether or not to draw the plots in bins of nvtx. Default: False", type=bool, default=False)

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    filezmumu = args.dir + "/all_ZToMuMu.root"
    if args.lumi != '':
        toplabel="#sqrt{s} = 13.6 TeV, L_{int} = " + args.lumi #+ " fb^{-1}"
    else:
        toplabel="#sqrt{s} = 13.6 TeV"

    # NVTX distribution:
#    drawplots.makedist(
#            inputFiles_list = [filezmumu],
#            saveplot = True,
#            h1d = ['h_nvtx'],
#            xtitle = 'N_{vtx}',
#            ytitle = 'Events',
#            top_label = toplabel,
#            plotname = 'L1Mu_nvtx',
#            dirname = args.dir + '/plotsL1Run3',
#            )

    for r in config['Regions']:
        region = config['Regions'][r]
        eta_range = "eta{}to{}".format(region[0], region[1]).replace(".","p")
        eta_label = '{{{} #leq | #eta^{{#mu}}(reco)| < {}}}'.format(region[0], region[1])

        #print(r)
        #print(region)
        #print(eta_range)
        #print(eta_label)

        if config['Efficiency']:

            # Efficiency vs Run Number
            drawplots.makeeff(
                inputFiles_list = [filezmumu],
                saveplot = True,
                dirname = args.dir + '/plotsL1Run3',
                den = ['h_PlateauEffVsRunNb_Denominator_AllQual_plots_{}'.format(eta_range)],
                num = ['h_PlateauEffVsRunNb_Numerator_{}_plots_{}'.format(qual, eta_range) for qual in config['Qualities']],
                xtitle = 'run number',
                ytitle = 'Efficiency',
                legendlabels = [label(qual) for qual in config['Qualities']],
                extralabel = "#splitline{{Z#rightarrow#mu#mu, p_{{T}}^{{#mu}}(reco) #geq 27 GeV}}{}".format(eta_label),
                top_label = toplabel,
                plotname = "L1Mu_EffVsRunNb_{}".format(r),
                )

        for qual in config['Qualities']:
            if config['TurnOns']:
                
                # Efficiency vs pT
                # all eta ranges and all qualities
                drawplots.makeeff(
                    inputFiles_list = [filezmumu],
                    saveplot = True,
                    dirname = args.dir + '/plotsL1Run3',
                    den = ['h_{}_plots_{}'.format(qual, eta_range)],
                    num = ['h_{}_plots_{}_l1thrgeq{}'.format(qual, eta_range, thr) for thr in  config['Thresholds']],
                    xtitle = 'p_{T}^{#mu}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = ['p_{{T}}^{{L1 #mu}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                    axisranges = [0, 500],
                    extralabel = "#splitline{{Z#rightarrow#mu#mu, {}}}{}".format(label(qual), eta_label),
                    setlogx = True,
                    top_label = toplabel,
                    plotname = 'L1Mu_TurnOn{}_{}'.format(qual, r) ,
                    )

                # same thing, zoom on the 0 - 50 GeV region in pT
                drawplots.makeeff(
                    inputFiles_list = [filezmumu],
                    saveplot = True,
                    dirname = args.dir + '/plotsL1Run3',
                    den = ['h_{}_plots_{}'.format(qual, eta_range)],
                    num = ['h_{}_plots_{}_l1thrgeq{}'.format(qual, eta_range, thr) for thr in  config['Thresholds']],
                    xtitle = 'p_{T}^{#mu}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = ['p_{{T}}^{{L1 #mu}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                    axisranges = [0, 50],
                    extralabel = "#splitline{{Z#rightarrow#mu#mu, {}}}{}".format(label(qual), eta_label),
                    setlogx = True,
                    top_label = toplabel,
                    plotname = 'L1Mu_TurnOn{}_{}_Zoom'.format(qual, r) ,
                    )

                # TODO: add nvtx plots

    if config['Efficiency']:
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['h_Mu22_EtaPhi_Numerator'],
            den = ['h_Mu22_EtaPhi_Denominator'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = '#phi^{#mu}(reco)',
            ztitle = 'L1Mu22 efficiency (p_{T}^{#mu}(reco) > 27 GeV)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu_EffVsEtaPhi',
            axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
            )

    if config['Prefiring']:

        # Postfiring vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Mu10to21_bxplus1_etaphi'],
            den = ['L1Mu10to21_bx0_etaphi'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = '#phi^{#mu}(reco)',
            ztitle = 'bx+1 / (bx0 or bx+1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu_PostfiringVsEtaPhi',
            axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
            addnumtoden = True,
            )

        # Prefiring vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Mu10to21_bxmin1_etaphi'],
            den = ['L1Mu10to21_bx0_etaphi'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = '#phi^{#mu}(reco)',
            ztitle = 'bx-1 / (bx0 or bx-1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu_PrefiringVsEtaPhi',
            axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
            addnumtoden = True,
            )
       
        # Postfiring vs Eta
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Mu10to21_bxplus1_eta'],
            den = ['L1Mu10to21_bx0_eta'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = 'bx+1 / (bx0 or bx+1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu_PostfiringVsEta',
            axisranges = [-2.4, 2.4, 0, 0.1],
            addnumtoden = True,
            )

        # Prefiring vs Eta
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Mu10to21_bxmin1_eta'],
            den = ['L1Mu10to21_bx0_eta'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = 'bx-1 / (bx0 or bx-1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu_PrefiringVsEta',
            axisranges = [-2.4, 2.4, 0, 0.1],
            addnumtoden = True,
            )
        
        # Same thing, for Mu 22
        # Postfiring vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Mu22_bxplus1_etaphi'],
            den = ['L1Mu22_bx0_etaphi'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = '#phi^{#mu}(reco)',
            ztitle = 'bx+1 / (bx0 or bx+1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > 22, L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu22_PostfiringVsEtaPhi',
            axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
            addnumtoden = True,
            )

        # Prefiring vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Mu22_FirstBunchInTrain_bxmin1_etaphi'],
            den = ['L1Mu22_bx0_etaphi'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = '#phi^{#mu}(reco)',
            ztitle = 'bx-1 / (bx0 or bx-1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > 22, L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu22_PrefiringVsEtaPhi',
            axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
            addnumtoden = True,
            )
       
        # Postfiring vs Eta
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Mu22_bxplus1_eta'],
            den = ['L1Mu22_bx0_eta'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = 'bx+1 / (bx0 or bx+1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > 22, L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu22_PostfiringVsEta',
            axisranges = [-2.4, 2.4, 0, 0.1],
            addnumtoden = True,
            )

        # Prefiring vs Eta
        drawplots.makeeff(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1Mu22_FirstBunchInTrain_bxmin1_eta'],
            den = ['L1Mu22_bx0_eta'],
            xtitle = '#eta^{#mu}(reco)',
            ytitle = 'bx-1 / (bx0 or bx-1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > 22, L1 Qual. #geq 12}',
            top_label = toplabel,
            plotname = 'L1Mu22_PrefiringVsEta',
            axisranges = [-2.4, 2.4, 0, 0.1],
            addnumtoden = True,
            )


    if config['Response'] and 'AllQual' in config['Qualities']:

        regions = config['Regions'].values()
        eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in regions]
        eta_labels = ['{} #leq | #eta| < {}'.format(region[0], region[1]) for region in regions]

        # Resolution Vs Pt
        drawplots.makeresol(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            h2d = ['h_ResponseVsPt_AllQual_plots_{}'.format(eta_range) for eta_range in eta_ranges],
            xtitle = 'p_{T}^{reco muon} (GeV)',
            ytitle = '(p_{T}^{L1Mu}/p_{T}^{reco muon})',
            extralabel = '#splitline{Z#rightarrow#mu#mu}{All qual.}',
            legendlabels = eta_labels,
            top_label = toplabel,
            plotname = 'L1Mu_ResponseVsPt',
            axisranges = [0, 100, 0, 1.6], 
            )

        # Resolution Vs RunNb
        drawplots.makeresol(
            inputFiles_list = [filezmumu],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            h2d = ['h_ResponseVsRunNb_AllQual_plots_{}'.format(eta_range) for eta_range in eta_ranges],
            xtitle = 'run number',
            ytitle = '(p_{T}^{L1Mu}/p_{T}^{reco muon})',
            extralabel = '#splitline{Z#rightarrow#mu#mu}{All qual.}',
            legendlabels = eta_labels,
            top_label = toplabel,
            plotname = 'L1Mu_ResponseVsPt',
            axisranges = [355374, 362760, 0, 2],
            )


def label(qual):
    labels = {
            'AllQual': 'All qual.',
            'Qual8': 'Qual. #geq 8',
            'Qual12': 'Qual. #geq 12',
            }

    if qual in labels:
        return(labels[qual])
    else:
        return('')

if __name__ == '__main__':
    main()
