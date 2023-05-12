# make_ZToEE_plots.py, a program to draw the L1Studies plots obtained from the histograms extracted from NanoAOD

import yaml
import drawplots
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-d", "--dir", dest="dir", help="The directory to read the inputs files from and draw the plots to", type=str, default='./')
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default='../config_cards/full_ZToEE.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')
    parser.add_argument("--plot_nvtx", dest="plot_nvtx", help="Whether or not to draw the plots in bins of nvtx. Default: False", type=bool, default=False)

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir + "/all_ZToEE.root"
    if args.lumi != '':
        toplabel="#sqrt{s} = 13.6 TeV, L_{int} = " + args.lumi #+ " fb^{-1}"
    else:
        toplabel="#sqrt{s} = 13.6 TeV"

    # NVTX distribution:
#    drawplots.makedist(
#            inputFiles_list = [input_file],
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
        eta_label = '{{{} #leq | #eta^{{e}}(reco)| < {}}}'.format(region[0], region[1])

        #print(r)
        #print(region)
        #print(eta_range)
        #print(eta_label)

        if config['Efficiency']:

            # Efficiency vs Run Number
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + '/plotsL1Run3',
                den = ['h_PlateauEffVsRunNb_Denominator_EGNonIso_plots_{}'.format(eta_range)],
                num = ['h_PlateauEffVsRunNb_Numerator_{}_plots_{}'.format(iso, eta_range) for iso in config['Isos']],
                xtitle = 'run number',
                ytitle = 'Efficiency',
                legendlabels = [label(iso) for iso in config['Isos']],
                extralabel = "#splitline{{Z#rightarrowee, p_{{T}}^{{e}}(reco) #geq 35 GeV}}{}".format(eta_label),
                top_label = toplabel,
                plotname = "L1EG_EffVsRunNb_{}".format(r),
                )

        for iso in config['Isos']:
            if config['TurnOns']:
                
                # Efficiency vs pT
                # all eta ranges and all qualities
                drawplots.makeeff(
                    inputFiles_list = [input_file],
                    saveplot = True,
                    dirname = args.dir + '/plotsL1Run3',
                    den = ['h_{}_plots_{}'.format(iso, eta_range)],
                    num = ['h_{}_plots_{}_l1thrgeq{}'.format(iso, eta_range, thr) for thr in  config['Thresholds']],
                    xtitle = 'p_{T}^{e}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = ['p_{{T}}^{{L1 e}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                    #axisranges = [0, 500],
                    extralabel = "#splitline{{Z#rightarrowee, {}}}{}".format(label(iso), eta_label),
                    setlogx = True,
                    top_label = toplabel,
                    plotname = 'L1EG_TurnOn{}_{}'.format(iso, r) ,
                    )

                # same thing, zoom on the 0 - 50 GeV region in pT
                drawplots.makeeff(
                    inputFiles_list = [input_file],
                    saveplot = True,
                    dirname = args.dir + '/plotsL1Run3',
                    den = ['h_{}_plots_{}'.format(iso, eta_range)],
                    num = ['h_{}_plots_{}_l1thrgeq{}'.format(iso, eta_range, thr) for thr in  config['Thresholds']],
                    xtitle = 'p_{T}^{e}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = ['p_{{T}}^{{L1 e}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                    axisranges = [5, 50],
                    extralabel = "#splitline{{Z#rightarrowee, {}}}{}".format(label(iso), eta_label),
                    setlogx = True,
                    top_label = toplabel,
                    plotname = 'L1EG_TurnOn{}_{}_Zoom'.format(iso, r) ,
                    )

                # TODO: add nvtx plots

    if config['Efficiency']:
        # Efficiency vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['h_EG25_EtaPhi_Numerator'],
            den = ['h_EG25_EtaPhi_Denominator'],
            xtitle = '#eta^{e}(reco)',
            ytitle = '#phi^{e}(reco)',
            ztitle = 'L1Mu22 efficiency (p_{T}^{e}(reco) > 30 GeV)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrowee}{L1 EG Tight Iso}',
            top_label = toplabel,
            plotname = 'L1EG_EffVsEtaPhi',
            axisranges = [-2.5, 2.5, -3.1416, 3.1416, 0, 1.1],
            )

    if config['Prefiring']:

        # Postfiring vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1EG15to26_bxplus1_etaphi'],
            den = ['L1EG15to26_bx0_etaphi'],
            xtitle = '#eta^{e}(reco)',
            ytitle = '#phi^{e}(reco)',
            ztitle = 'bx+1 / (bx0 or bx+1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
            top_label = toplabel,
            plotname = 'L1EG_PostfiringVsEtaPhi',
            axisranges = [-2.5, 2.5, -3.1416, 3.1416, 0, 1.1],
            addnumtoden = True,
            )

        # Prefiring vs Eta Phi
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1EG15to26_bxmin1_etaphi'],
            den = ['L1EG15to26_bx0_etaphi'],
            xtitle = '#eta^{e}(reco)',
            ytitle = '#phi^{e}(reco)',
            ztitle = 'bx-1 / (bx0 or bx-1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
            top_label = toplabel,
            plotname = 'L1EG_PrefiringVsEtaPhi',
            axisranges = [-2.5, 2.5, -3.1416, 3.1416, 0, 1.1],
            addnumtoden = True,
            )
       
        # Postfiring vs Eta 
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1EG15to26_bxplus1_eta'],
            den = ['L1EG15to26_bx0_eta'],
            xtitle = '#eta^{e}(reco)',
            ytitle = 'bx+1 / (bx0 or bx+1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
            top_label = toplabel,
            plotname = 'L1EG_PostfiringVsEta',
            axisranges = [-2.5, 2.5, 0, 0.1],
            addnumtoden = True,
            )

        # Prefiring vs Eta 
        drawplots.makeeff(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            num = ['L1EG15to26_bxmin1_eta'],
            den = ['L1EG15to26_bx0_eta'],
            xtitle = '#eta^{e}(reco)',
            ytitle = 'bx-1 / (bx0 or bx-1)',
            legendlabels = [''],
            extralabel = '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
            top_label = toplabel,
            plotname = 'L1EG_PrefiringVsEta',
            axisranges = [-2.5, 2.5, 0, 0.1],
            addnumtoden = True,
            )

    if config['Response'] and 'EGNonIso' in config['Isos']:

        regions = config['Regions'].values()
        eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in regions]
        eta_labels = ['{} #leq | #eta| < {}'.format(region[0], region[1]) for region in regions]

        # Resolution Vs Pt
        drawplots.makeresol(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            h2d = ['h_ResponseVsPt_EGNonIso_plots_{}'.format(eta_range) for eta_range in eta_ranges],
            xtitle = 'p_{T}^{reco e} (GeV)',
            ytitle = '(p_{T}^{L1EG}/p_{T}^{reco e})',
            extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
            legendlabels = eta_labels,
            top_label = toplabel,
            plotname = 'L1EG_ResponseVsPt',
            axisranges = [0, 100, 0, 1.6], 
            )

        # Resolution Vs RunNb
        drawplots.makeresol(
            inputFiles_list = [input_file],
            saveplot = True,
            dirname = args.dir + '/plotsL1Run3',
            h2d = ['h_ResponseVsRunNb_EGNonIso_plots_{}'.format(eta_range) for eta_range in eta_ranges],
            xtitle = 'run number',
            ytitle = '(p_{T}^{L1EG}/p_{T}^{reco e})',
            extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
            legendlabels = eta_labels,
            top_label = toplabel,
            plotname = 'L1EG_ResponseVsRunNb',
            axisranges = [355374, 362760, 0, 2],
            )


def label(iso):
    labels = {
            'EGNonIso': 'Non iso',
            'EGLoosIso': 'Loose iso',
            'EGTightIso': 'Tight iso',
            }

    if iso in labels:
        return(labels[iso])
    else:
        return('')

if __name__ == '__main__':
    main()
