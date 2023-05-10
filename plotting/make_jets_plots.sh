#!/bin/bash
# make_jets_plots.sh, draw L1Studies plots from histos obtained with the MuonJet and PhotonJet skims

# CL arguments
dir=$1

lumi=$2
nvtx_suffix=$3

# if there is a nvtx_suffix, add the corresponding argument in the command aliases. Otherwise leave it blank
echo "$nvtx_suffix"
if [ -z "$nvtx_suffix" ]
then
    nvtx_arg=""
else
    nvtx_arg="--nvtx_suffix $nvtx_suffix"
fi

# some aliases (the drawplot.py must be in the same directory as the script, otherwise modify the path)
makeeff="python3 $PWD/drawplots.py -t efficiency --saveplot True $nvtx_arg"
makeprof="python3 $PWD/drawplots.py -t profilex_fromh2 --saveplot True $nvtx_arg"
makeresol="python3 $PWD/drawplots.py -t resolvsx --saveplot True $nvtx_arg"
makedist="python3 $PWD/drawplots.py -t distribution --saveplot True $nvtx_arg"

# move to workdir
cd $dir
filemujet=all_MuonJet.root
filegamjet=all_PhotonJet.root

# set some labels
toplabel="#sqrt{s} = 13.6 TeV, L_{int} = $lumi fb^{-1}"
#top_eg=$2
#top_mu=$3

muselection='#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24'
photonselection='#geq 1 tight #gamma (p_{T} > 115 GeV, |#eta| < 1.479)'

for skim in "FromEGamma" "FromSingleMuon"
do
    case $skim in 
        "FromSingleMuon")
            selection_label=$muselection
            file=$filemujet
            #toplabel=$top_mu
            ;;
        "FromEGamma")
            selection_label=$photonselection
            file=$filegamjet
            #toplabel=$top_eg
            ;;
        *)
            ;;
    esac

    if [ $skim == "FromEGamma" ]
    then
        $makeprof \
            -i $file\
            --h2d h_L1PtBalanceVsRunNb_eta0p0to1p3$nvtx_suffix h_L1PtBalanceVsRunNb_eta1p3to2p5$nvtx_suffix h_L1PtBalanceVsRunNb_eta2p5to3p0$nvtx_suffix h_L1PtBalanceVsRunNb_eta3p0to3p5$nvtx_suffix h_L1PtBalanceVsRunNb_eta3p5to4p0$nvtx_suffix h_L1PtBalanceVsRunNb_eta4p0to5p0$nvtx_suffix \
            --xtitle 'run number' \
            --ytitle '(p_{T}^{L1 jet}/p_{T}^{reco #gamma})' \
            --extralabel "#splitline{$selection_label, PFMET<50 GeV}{p_{T}^{jet} > 30 GeV, #Delta#phi(#gamma, jet) > 2.9}" \
            --legend '0 #leq |#eta| < 1.3' '1.3 #leq |#eta| < 2.5' '2.5 #leq |#eta| < 3.0' '3.0 #leq |#eta| < 3.5' '3.5 #leq |#eta| < 4.0' '4.0 #leq |#eta| < 5.0' \
            --toplabel "$toplabel" \
            --axisrange 320673 325173 0 1.5\
            --plotname L1Jet_FromEGamma_PtBalancevsRunNb
            #--axisrange 355374 363000 0 1.5\

        $makeprof \
            -i $file\
            --h2d h_L1PtBalanceVsRunNb_singlejet_eta0p0to1p3$nvtx_suffix h_L1PtBalanceVsRunNb_singlejet_eta1p3to2p5$nvtx_suffix h_L1PtBalanceVsRunNb_singlejet_eta2p5to3p0$nvtx_suffix h_L1PtBalanceVsRunNb_singlejet_eta3p0to3p5$nvtx_suffix h_L1PtBalanceVsRunNb_singlejet_eta3p5to4p0$nvtx_suffix h_L1PtBalanceVsRunNb_singlejet_eta4p0to5p0$nvtx_suffix \
            --xtitle 'run number' \
            --ytitle '(p_{T}^{L1 jet}/p_{T}^{reco #gamma})' \
            --extralabel "#splitline{$selection_label, PFMET<50 GeV}{= 1 clean jet, p_{T}^{jet} > 30 GeV, #Delta#phi(#gamma, jet) > 2.9}" \
            --legend '0 #leq |#eta| < 1.3' '1.3 #leq |#eta| < 2.5' '2.5 #leq |#eta| < 3.0' '3.0 #leq |#eta| < 3.5' '3.5 #leq |#eta| < 4.0' '4.0 #leq |#eta| < 5.0' \
            --toplabel "$toplabel" \
            --axisrange 320673 325173 0 1.5\
            --plotname L1Jet_FromEGamma_PtBalancevsRunNb_singlejet
            #--axisrange 355374 363000 0 1.5\
    fi

    continue

    # distribution of nvtx
    if [ -z "$nvtx_suffix" ]
    then
        $makedist -i $file \
            --h1d h_nvtx \
            --xtitle 'N_{vtx}' \
            --ytitle 'Events' \
            --toplabel "$toplabel" \
            --plotname L1Jet_"$skim"_nvtx
    fi

    for range in "barrel" "endcap1" "endcap2" "hf1" "hf2" "hf3"
    do

        case $range in 
            "barrel")
                eta_range="eta0p0to1p3"
                eta_label='0.0 #leq |#eta^{jet}(reco)| < 1.3'
                pt_max=2000
                ;;
            "endcap1")
                eta_range="eta1p3to2p5"
                eta_label='1.3 #leq |#eta^{jet}(reco)| < 2.5'
                pt_max=1000
                ;;
            "endcap2")
                eta_range="eta2p5to3p0"
                eta_label='2.5 #leq |#eta^{jet}(reco)| < 3.0'
                pt_max=500
                ;;
            "hf1")
                eta_range="eta3p0to3p5"
                eta_label='3.0 #leq |#eta^{jet}(reco)| < 3.5'
                pt_max=500
                ;;
            "hf2")
                eta_range="eta3p5to4p0"
                eta_label='3.5 #leq |#eta^{jet}(reco)| < 4.0'
                pt_max=500
                ;;
            "hf3")
                eta_range="eta4p0to5p0"
                eta_label='4.0 #leq |#eta^{jet}(reco)| < 5.0'
                pt_max=500
                ;;
            *)
                ;;
        esac

        # Not enough stat in hf2/hf3 for MuonJet
        if [ $skim == "FromSingleMuon" ] && { [ $range == "hf2" ] || [ $range == "hf3" ]; }
        then
            continue
        fi

        # Efficiency vs Run Number
        # all eta ranges

        $makeeff -i $file \
            --den h_PlateauEffVsRunNb_Denominator_Jet_plots_"$eta_range" \
            --num h_PlateauEffVsRunNb_Numerator_Jet_plots_"$eta_range" \
            --xtitle 'run number' \
            --ytitle 'Efficiency' \
            --legend '' \
            --extralabel "#splitline{$selection_label, p_{T}^{jet} > 30 GeV}{$eta_label}" \
            --toplabel "$toplabel" \
            --plotname L1Jet_"$skim"_EffVsRunNb_"$range"


        # Efficiency vs pT
        # all eta ranges
        if [ $pt_max -gt 500 ]
        then 
            logx="--setlogx True"
        else
            logx=""
        fi

        $makeeff -i $file \
            --num h_Jet_plots_"$eta_range"_l1thrgeq30p0 h_Jet_plots_"$eta_range"_l1thrgeq40p0 h_Jet_plots_"$eta_range"_l1thrgeq60p0 h_Jet_plots_"$eta_range"_l1thrgeq80p0 h_Jet_plots_"$eta_range"_l1thrgeq100p0 h_Jet_plots_"$eta_range"_l1thrgeq120p0 h_Jet_plots_"$eta_range"_l1thrgeq140p0 h_Jet_plots_"$eta_range"_l1thrgeq160p0 h_Jet_plots_"$eta_range"_l1thrgeq180p0 h_Jet_plots_"$eta_range"_l1thrgeq200p0 \
            --den h_Jet_plots_"$eta_range" \
            --xtitle 'p_{T}^{jet}(reco) (GeV)' \
            --ytitle 'Efficiency' \
            --legend 'p_{T}^{L1 jet} #geq 30 GeV' 'p_{T}^{L1 jet} #geq 40 GeV' 'p_{T}^{L1 jet} #geq 60 GeV' 'p_{T}^{L1 jet} #geq 80 GeV' 'p_{T}^{L1 jet} #geq 100 GeV' 'p_{T}^{L1 jet} #geq 120 GeV' 'p_{T}^{L1 jet} #geq 140 GeV' 'p_{T}^{L1 jet} #geq 160 GeV' 'p_{T}^{L1 jet} #geq 180 GeV' 'p_{T}^{L1 jet} #geq 200 GeV' \
            --axisranges 30 $pt_max \
            --extralabel "#splitline{$selection_label, p_{T}^{jet} > 30 GeV}{$eta_label}" \
            --toplabel "$toplabel" \
            $logx \
            --plotname L1Jet_"$skim"_TurnOn_"$range"

        # Vs PU
        if [ -z "$nvtx_suffix" ]
        then

            $makeeff -i $file \
                --num h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx10to20 h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx20to30 h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx30to40 h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx40to50 h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx50to60 \
                --den h_Jet_plots_"$eta_range"_nvtx10to20 h_Jet_plots_"$eta_range"_nvtx20to30 h_Jet_plots_"$eta_range"_nvtx30to40 h_Jet_plots_"$eta_range"_nvtx40to50 h_Jet_plots_"$eta_range"_nvtx50to60 \
                --xtitle 'p_{T}^{jet}(reco) (GeV)' \
                --ytitle 'Efficiency' \
                --legend 'nvtx #in #[]{10, 20}' 'nvtx #in #[]{20, 30}' 'nvtx #in #[]{30, 40}' 'nvtx #in #[]{40, 50}' 'nvtx #in #[]{50, 60}' \
                --axisranges 30 $pt_max \
                --extralabel "#splitline{$selection_label, p_{T}^{jet} > 30 GeV}{#splitline{$eta_label}{p_{T}^{L1 jet} #geq 40 GeV}}" \
                --toplabel "$toplabel" \
                $logx \
                --plotname L1Jet_"$skim"_TurnOn_"$range"_vsPU

        fi

        # same thing, zoom on the 0 - 300 GeV region in pT
        if [ $pt_max -gt 500 ]
        then
            $makeeff -i $file \
                --num h_Jet_plots_"$eta_range"_l1thrgeq30p0 h_Jet_plots_"$eta_range"_l1thrgeq40p0 h_Jet_plots_"$eta_range"_l1thrgeq60p0 h_Jet_plots_"$eta_range"_l1thrgeq80p0 h_Jet_plots_"$eta_range"_l1thrgeq100p0 h_Jet_plots_"$eta_range"_l1thrgeq120p0 h_Jet_plots_"$eta_range"_l1thrgeq140p0 h_Jet_plots_"$eta_range"_l1thrgeq160p0 h_Jet_plots_"$eta_range"_l1thrgeq180p0 h_Jet_plots_"$eta_range"_l1thrgeq200p0 \
                --den h_Jet_plots_"$eta_range" \
                --xtitle 'p_{T}^{jet}(reco) (GeV)' \
                --ytitle 'Efficiency' \
                --legend 'p_{T}^{L1 jet} #geq 30 GeV' 'p_{T}^{L1 jet} #geq 40 GeV' 'p_{T}^{L1 jet} #geq 60 GeV' 'p_{T}^{L1 jet} #geq 80 GeV' 'p_{T}^{L1 jet} #geq 100 GeV' 'p_{T}^{L1 jet} #geq 120 GeV' 'p_{T}^{L1 jet} #geq 140 GeV' 'p_{T}^{L1 jet} #geq 160 GeV' 'p_{T}^{L1 jet} #geq 180 GeV' 'p_{T}^{L1 jet} #geq 200 GeV' \
                --axisranges 30 500 \
                --extralabel "#splitline{$selection_label, p_{T}^{jet} > 30 GeV}{$eta_label}" \
                --toplabel "$toplabel" \
                --plotname L1Jet_"$skim"_TurnOn_"$range"_Zoom

            if [ -z "$nvtx_suffix" ]
            then

                # Vs PU
                $makeeff -i $file \
                    --num h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx10to20 h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx20to30 h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx30to40 h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx40to50 h_Jet_plots_"$eta_range"_l1thrgeq40p0_nvtx50to60 \
                    --den h_Jet_plots_"$eta_range"_nvtx10to20 h_Jet_plots_"$eta_range"_nvtx20to30 h_Jet_plots_"$eta_range"_nvtx30to40 h_Jet_plots_"$eta_range"_nvtx40to50 h_Jet_plots_"$eta_range"_nvtx50to60 \
                    --xtitle 'p_{T}^{jet}(reco) (GeV)' \
                    --ytitle 'Efficiency' \
                    --legend 'nvtx #in #[]{10, 20}' 'nvtx #in #[]{20, 30}' 'nvtx #in #[]{30, 40}' 'nvtx #in #[]{40, 50}' 'nvtx #in #[]{50, 60}' \
                    --axisranges 30 500 \
                    --extralabel "#splitline{$selection_label, p_{T}^{jet} > 30 GeV}{#splitline{$eta_label}{p_{T}^{L1 jet} #geq 40 GeV}}" \
                    --toplabel "$toplabel" \
                    --plotname L1Jet_"$skim"_TurnOn_"$range"_vsPU_Zoom
            fi
        fi

    done

    # Efficiency vs Eta Phi

    case $skim in 
        "FromSingleMuon")
            PtThreshold=50
            ;;
        "FromEGamma")
            PtThreshold=100
            ;;
        *)
            ;;
    esac

    $makeeff -i $file \
        --num h_L1Jet"$PtThreshold"vsEtaPhi_Numerator \
        --den h_L1Jet"$PtThreshold"vsEtaPhi_EtaRestricted \
        --xtitle '#eta^{jet}(reco)' \
        --ytitle '#phi^{jet}(reco)' \
        --ztitle "L1Jet$PtThreshold efficiency" \
        --legend '' \
        --extralabel "#splitline{$selection_label}{p_{T}^{jet} > 30 GeV}" \
        --toplabel "$toplabel" \
        --plotname L1Jet_"$skim"_EffVsEtaPhi \
        --axisranges -5 5 -3.1416 3.1416 0 1.1

    # Postfiring vs Eta Phi

    $makeeff -i $file \
        --num L1Jet100to150_bxplus1_etaphi  \
        --den L1Jet100to150_bx0_etaphi  \
        --xtitle '#eta^{jet}(reco)' \
        --ytitle '#phi^{jet}(reco)' \
        --ztitle 'bx+1 / (bx0 or bx+1)' \
        --legend '' \
        --extralabel "#splitline{$selection_label}{p_{T}^{jet} > 30 GeV}" \
        --toplabel "$toplabel" \
        --plotname  L1Jet_"$skim"_PostfiringVsEtaPhi \
        --axisranges -5 5 -3.1416 3.1416 0 1.1 \
        --addnumtoden True

    # Prefiring vs Eta Phi

    $makeeff -i $file \
        --num L1Jet100to150_bxmin1_etaphi  \
        --den L1Jet100to150_bx0_etaphi  \
        --xtitle '#eta^{jet}(reco)' \
        --ytitle '#phi^{jet}(reco)' \
        --ztitle 'bx-1 / (bx0 or bx-1)' \
        --legend '' \
        --extralabel "#splitline{$selection_label}{p_{T}^{jet} > 30 GeV}" \
        --toplabel "$toplabel" \
        --plotname  L1Jet_"$skim"_PrefiringVsEtaPhi \
        --axisranges -5 5 -3.1416 3.1416 0 1.1 \
        --addnumtoden True

    # Post vs Eta only

    $makeeff -i $file \
        --num L1Jet100to150_bxplus1_eta  \
        --den L1Jet100to150_bx0_eta  \
        --xtitle '#eta^{jet}(reco)' \
        --ytitle 'bx+1 / (bx0 or bx+1)' \
        --legend '' \
        --extralabel "#splitline{$selection_label}{p_{T}^{jet} > 30 GeV}" \
        --toplabel "$toplabel" \
        --plotname  L1Jet_"$skim"_PostfiringVsEta \
        --axisranges -5 5 0 1.1 \
        --addnumtoden True

    # Prefiring vs Eta only

    $makeeff -i $file \
        --num L1Jet100to150_bxmin1_eta  \
        --den L1Jet100to150_bx0_eta  \
        --xtitle '#eta^{jet}(reco)' \
        --ytitle 'bx-1 / (bx0 or bx-1)' \
        --legend '' \
        --extralabel "#splitline{$selection_label}{p_{T}^{jet} > 30 GeV}" \
        --toplabel "$toplabel" \
        --plotname  L1Jet_"$skim"_PrefiringVsEta \
        --axisranges -5 5 0 1.1 \
        --addnumtoden True

    # Response vs Pt

    $makeresol \
        -i $file \
        --h2d h_ResponseVsPt_Jet_plots_eta0p0to1p3 h_ResponseVsPt_Jet_plots_eta1p3to2p5 h_ResponseVsPt_Jet_plots_eta2p5to3p0 h_ResponseVsPt_Jet_plots_eta3p0to3p5 h_ResponseVsPt_Jet_plots_eta3p5to4p0 h_ResponseVsPt_Jet_plots_eta4p0to5p0 \
        --xtitle 'p_{T}^{reco jet} (GeV)' \
        --ytitle '(p_{T}^{L1 jet}/p_{T}^{reco jet})' \
        --legend '0 #leq |#eta| < 1.3' '1.3 #leq |#eta| < 2.5' '2.5 #leq |#eta| < 3.0' '3.0 #leq |#eta| < 3.5' '3.5 #leq |#eta| < 4.0' '4.0 #leq |#eta| < 5.0' \
        --legendpos "top" \
        --toplabel "$toplabel" \
        --axisrange 0 200 0 1.6 \
        --plotname L1Jet_"$skim"_ResponseVsPt

    # Response vs Run Number
    #
    $makeresol \
        -i $file \
        --h2d h_ResponseVsRunNb_Jet_plots_eta0p0to1p3 h_ResponseVsRunNb_Jet_plots_eta1p3to2p5 h_ResponseVsRunNb_Jet_plots_eta2p5to3p0 h_ResponseVsRunNb_Jet_plots_eta3p0to3p5 h_ResponseVsRunNb_Jet_plots_eta3p5to4p0 h_ResponseVsRunNb_Jet_plots_eta4p0to5p0 \
        --xtitle 'run number' \
        --ytitle '(p_{T}^{L1 jet}/p_{T}^{reco jet})' \
        --legend '0 #leq |#eta| < 1.3' '1.3 #leq |#eta| < 2.5' '2.5 #leq |#eta| < 3.0' '3.0 #leq |#eta| < 3.5' '3.5 #leq |#eta| < 4.0' '4.0 #leq |#eta| < 5.0' \
        --legendpos "top" \
        --toplabel "$toplabel" \
        --axisrange 355374 362760 0 2 \
        --plotname L1Jet_"$skim"_ResponseVsRunNb 

    # Zoomed version

    $makeresol \
        -i $file \
        --h2d h_ResponseVsRunNb_Jet_plots_eta0p0to1p3 h_ResponseVsRunNb_Jet_plots_eta1p3to2p5 \
        --xtitle 'run number' \
        --ytitle '(p_{T}^{L1 jet}/p_{T}^{reco jet})' \
        --legend '0 #leq |#eta| < 1.3' '1.3 #leq |#eta| < 2.5' \
        --legendpos "top" \
        --toplabel "$toplabel" \
        --axisrange 355374 362760 0.8 1.1 \
        --plotname L1Jet_"$skim"_ResponseVsRunNb_Zoom
done

#$makeresol \
#    -i $filegamjet \
#    --h2d h_ResponseVsPt_big_bins_Jet_plots_eta0p0to1p3 h_ResponseVsPt_big_bins_Jet_plots_eta1p3to2p5 h_ResponseVsPt_big_bins_Jet_plots_eta2p5to3p0 h_ResponseVsPt_big_bins_Jet_plots_eta3p0to3p5 h_ResponseVsPt_big_bins_Jet_plots_eta3p5to4p0 h_ResponseVsPt_big_bins_Jet_plots_eta4p0to5p0 \
#    --xtitle 'p_{T}^{reco jet} (GeV)' \
#    --ytitle '(p_{T}^{L1 jet}/p_{T}^{reco jet})' \
#    --legend '0 #leq |#eta| < 1.3' '1.3 #leq |#eta| < 2.5' '2.5 #leq |#eta| < 3.0' '3.0 #leq |#eta| < 3.5' '3.5 #leq |#eta| < 4.0' '4.0 #leq |#eta| < 5.0' \
#    --legendpos "top" \
#    --toplabel "$top_eg" \
#    --axisrange 0 200 0 1.6 \
#    --plotname L1Jet_FromEGamma_ResponseVsPt_big_bins
