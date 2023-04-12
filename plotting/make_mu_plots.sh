#!/bin/bash
# make_mu_plots.sh, draw L1Studies plots from histos obtained with the ZToMuMu skim

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
makeresol="python3 $PWD/drawplots.py -t resolvsx --saveplot True $nvtx_arg"
makedist="python3 $PWD/drawplots.py -t distribution --saveplot True $nvtx_arg"

# move to workdir
cd $dir
filezmumu=all_ZToMuMu.root

toplabel="#sqrt{s} = 13.6 TeV, L_{int} = $lumi fb^{-1}"

if [ -z "$nvtx_suffix" ]
then
    $makedist -i $filezmumu \
        --h1d h_nvtx \
        --xtitle 'N_{vtx}' \
        --ytitle 'Events' \
        --toplabel "$toplabel" \
        --plotname L1Mu_nvtx
fi

for range in "EMTF" "BMTF" "OMTF"
do
    case $range in
        "EMTF")
            eta_range="eta1p24to2p4"
            eta_label='{1.24 #leq |#eta^{#mu}(reco)| < 2.4}'
            ;;

        "BMTF")
            eta_range="eta0p0to0p83"
            eta_label='{0 #leq |#eta^{#mu}(reco)| < 0.83}'
            ;;

        "OMTF")
            eta_range="eta0p83to1p24"
            eta_label='{0.83 #leq |#eta^{#mu}(reco)| < 1.24}'
            ;;

        *)
            ;;
    esac


    # Efficiency vs Run Number
    # all eta ranges

    $makeeff -i $filezmumu \
        --den h_PlateauEffVsRunNb_Denominator_AllQual_plots_"$eta_range" \
        --num h_PlateauEffVsRunNb_Numerator_AllQual_plots_"$eta_range" h_PlateauEffVsRunNb_Numerator_Qual8_plots_"$eta_range" h_PlateauEffVsRunNb_Numerator_Qual12_plots_"$eta_range"  \
        --xtitle 'run number' \
        --ytitle 'Efficiency' \
        --legend 'All qual.' 'Qual. #geq 8' 'Qual. #geq 12' \
        --extralabel "#splitline{Z#rightarrow#mu#mu, p_{T}^{#mu}(reco) #geq 27 GeV}$eta_label" \
        --toplabel "$toplabel" \
        --plotname L1Mu_EffVsRunNb_"$range"

    for Qual in "Qual12" "Qual8" "AllQual"
    do
        case $Qual in 
            "Qual12")
                qual_label='Qual. #geq 12'
                ;;

            "Qual8")
                qual_label='Qual. #geq 8'
                ;;

            "AllQual")
                qual_label='all Qual.'
                ;;

            *)
                ;;
        esac

        # Efficiency vs pT
        # all eta ranges and all qualities

        $makeeff -i $filezmumu \
            --den h_"$Qual"_plots_"$eta_range" \
            --num h_"$Qual"_plots_"$eta_range"_l1thrgeq3 h_"$Qual"_plots_"$eta_range"_l1thrgeq5 h_"$Qual"_plots_"$eta_range"_l1thrgeq10 h_"$Qual"_plots_"$eta_range"_l1thrgeq15 h_"$Qual"_plots_"$eta_range"_l1thrgeq20 h_"$Qual"_plots_"$eta_range"_l1thrgeq22 h_"$Qual"_plots_"$eta_range"_l1thrgeq26 \
            --xtitle 'p_{T}^{#mu}(reco) (GeV)' \
            --ytitle 'Efficiency' \
            --legend 'p_{T}^{L1 #mu} #geq 3 GeV' 'p_{T}^{L1 #mu} #geq 5 GeV' 'p_{T}^{L1 #mu} #geq 10 GeV' 'p_{T}^{L1 #mu} #geq 15 GeV' 'p_{T}^{L1 #mu} #geq 20 GeV' 'p_{T}^{L1 #mu} #geq 22 GeV' 'p_{T}^{L1 #mu} #geq 26 GeV' \
            --axisranges 0 500 \
            --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}$eta_label" \
            --setlogx True \
            --toplabel "$toplabel" \
            --plotname L1Mu_TurnOn"$Qual"_"$range"

        # same thing, zoom on the 0 - 50 GeV region in pT

        $makeeff -i $filezmumu \
            --den h_"$Qual"_plots_"$eta_range" \
            --num h_"$Qual"_plots_"$eta_range"_l1thrgeq3 h_"$Qual"_plots_"$eta_range"_l1thrgeq5 h_"$Qual"_plots_"$eta_range"_l1thrgeq10 h_"$Qual"_plots_"$eta_range"_l1thrgeq15 h_"$Qual"_plots_"$eta_range"_l1thrgeq20 h_"$Qual"_plots_"$eta_range"_l1thrgeq22 h_"$Qual"_plots_"$eta_range"_l1thrgeq26 \
            --xtitle 'p_{T}^{#mu}(reco) (GeV)' \
            --ytitle 'Efficiency' \
            --legend 'p_{T}^{L1 #mu} #geq 3 GeV' 'p_{T}^{L1 #mu} #geq 5 GeV' 'p_{T}^{L1 #mu} #geq 10 GeV' 'p_{T}^{L1 #mu} #geq 15 GeV' 'p_{T}^{L1 #mu} #geq 20 GeV' 'p_{T}^{L1 #mu} #geq 22 GeV' 'p_{T}^{L1 #mu} #geq 26 GeV' \
            --axisranges 0 50 \
            --setlogx True \
            --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}$eta_label" \
            --toplabel "$toplabel" \
            --plotname L1Mu_TurnOn"$Qual"_"$range"_Zoom

        # TurnOn, for different nvtx
        if [ -z "$nvtx_suffix" ]
        then

            $makeeff -i $filezmumu \
                --den h_"$Qual"_plots_"$eta_range"_nvtx10to20 h_"$Qual"_plots_"$eta_range"_nvtx20to30 h_"$Qual"_plots_"$eta_range"_nvtx30to40 h_"$Qual"_plots_"$eta_range"_nvtx40to50 h_"$Qual"_plots_"$eta_range"_nvtx50to60 \
                --num h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx10to20 h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx20to30 h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx30to40 h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx40to50 h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx50to60 \
                --xtitle 'p_{T}^{#mu}(reco) (GeV)' \
                --ytitle 'Efficiency' \
                --legend 'nvtx #in #[]{10, 20}' 'nvtx #in #[]{20, 30}' 'nvtx #in #[]{30, 40}' 'nvtx #in #[]{40, 50}' 'nvtx #in #[]{50, 60}' \
                --axisranges 0 500 \
                --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}{#splitline$eta_label{p_{T}^{L1 #mu} #geq 5 GeV}}" \
                --setlogx True \
                --toplabel "$toplabel" \
                --plotname L1Mu_TurnOn"$Qual"_"$range"_vsPU

            # same thing, zoom on the 0 - 50 GeV region in pT

            $makeeff -i $filezmumu \
                --den h_"$Qual"_plots_"$eta_range"_nvtx10to20 h_"$Qual"_plots_"$eta_range"_nvtx20to30 h_"$Qual"_plots_"$eta_range"_nvtx30to40 h_"$Qual"_plots_"$eta_range"_nvtx40to50 h_"$Qual"_plots_"$eta_range"_nvtx50to60 \
                --num h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx10to20 h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx20to30 h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx30to40 h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx40to50 h_"$Qual"_plots_"$eta_range"_l1thrgeq5_nvtx50to60 \
                --xtitle 'p_{T}^{#mu}(reco) (GeV)' \
                --ytitle 'Efficiency' \
                --legend 'nvtx #in #[]{10, 20}' 'nvtx #in #[]{20, 30}' 'nvtx #in #[]{30, 40}' 'nvtx #in #[]{40, 50}' 'nvtx #in #[]{50, 60}' \
                --axisranges 0 50 \
                --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}{#splitline$eta_label{p_{T}^{L1 #mu} #geq 5 GeV}}" \
                --setlogx True \
                --toplabel "$toplabel" \
                --plotname L1Mu_TurnOn"$Qual"_"$range"_vsPU_Zoom
        fi
    done
done

# Efficiency vs Eta Phi

$makeeff -i $filezmumu \
    --num h_Mu22_EtaPhi_Numerator \
    --den h_Mu22_EtaPhi_Denominator   \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle '#phi^{#mu}(reco)' \
    --ztitle 'L1Mu22 efficiency (p_{T}^{#mu}(reco) > 27 GeV)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu_EffVsEtaPhi \
    --axisranges -2.4 2.4 -3.1416 3.1416 0 1.1

# Postfiring vs Eta Phi

$makeeff -i $filezmumu \
    --num L1Mu10to21_bxplus1_etaphi  \
    --den L1Mu10to21_bx0_etaphi  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle '#phi^{#mu}(reco)' \
    --ztitle 'bx+1 / (bx0 or bx+1)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu_PostfiringVsEtaPhi \
    --axisranges -2.4 2.4 -3.1416 3.1416 0 1.1 \
    --addnumtoden True

# Prefiring vs Eta Phi

$makeeff -i $filezmumu \
    --num L1Mu10to21_bxmin1_etaphi  \
    --den L1Mu10to21_bx0_etaphi  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle '#phi^{#mu}(reco)' \
    --ztitle 'bx-1 / (bx0 or bx-1)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu_PrefiringVsEtaPhi \
    --axisranges -2.4 2.4 -3.1416 3.1416 0 1.1 \
    --addnumtoden True

# Postfiring vs Eta only

$makeeff -i $filezmumu \
    --num L1Mu10to21_bxplus1_eta  \
    --den L1Mu10to21_bx0_eta  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle 'bx+1 / (bx0 or bx+1)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu_PostfiringVsEta \
    --axisranges -2.5 2.5 0 0.1 \
    --addnumtoden True 

# Prefiring vs Eta only

$makeeff -i $filezmumu \
    --num L1Mu10to21_bxmin1_eta  \
    --den L1Mu10to21_bx0_eta  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle 'bx-1 / (bx0 or bx-1)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu_PrefiringVsEta \
    --axisranges -2.5 2.5 0 0.1 \
    --addnumtoden True 

# Same, for Mu 22
#
# Postfiring vs Eta Phi

$makeeff -i $filezmumu \
    --num L1Mu22_bxplus1_etaphi  \
    --den L1Mu22_bx0_etaphi  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle '#phi^{#mu}(reco)' \
    --ztitle 'bx+1 / (bx0 or bx+1)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > 22, L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu22_PostfiringVsEtaPhi \
    --axisranges -2.4 2.4 -3.1416 3.1416 0 1.1 \
    --addnumtoden True

# Prefiring vs Eta Phi

$makeeff -i $filezmumu \
    --num L1Mu22_bxmin1_etaphi  \
    --den L1Mu22_bx0_etaphi  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle '#phi^{#mu}(reco)' \
    --ztitle 'bx-1 / (bx0 or bx-1)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > 22, L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu22_PrefiringVsEtaPhi \
    --axisranges -2.4 2.4 -3.1416 3.1416 0 1.1 \
    --addnumtoden True

# Postfiring vs Eta only

$makeeff -i $filezmumu \
    --num L1Mu22_bxplus1_eta  \
    --den L1Mu22_bx0_eta  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle 'bx+1 / (bx0 or bx+1)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > 22, L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu22_PostfiringVsEta \
    --axisranges -2.5 2.5 0 0.1 \
    --addnumtoden True 

# Prefiring vs Eta only

$makeeff -i $filezmumu \
    --num L1Mu22_bxmin1_eta  \
    --den L1Mu22_bx0_eta  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle 'bx-1 / (bx0 or bx-1)' \
    --legend '' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > 22, L1 Qual.>= 12}' \
    --toplabel "$toplabel" \
    --plotname L1Mu22_PrefiringVsEta \
    --axisranges -2.5 2.5 0 0.1 \
    --addnumtoden True 


# Resolution vs Pt

$makeresol \
    -i $filezmumu \
    --h2d h_ResponseVsPt_AllQual_plots_eta0p0to0p83 h_ResponseVsPt_AllQual_plots_eta0p83to1p24 h_ResponseVsPt_AllQual_plots_eta1p24to2p4  \
    --xtitle 'p_{T}^{reco muon} (GeV)' \
    --ytitle '(p_{T}^{L1Mu}/p_{T}^{reco muon})' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{All qual.}' \
    --legend '0 #leq |#eta| < 0.83' '0.83 #leq |#eta| < 1.24' '1.24 #leq |#eta| < 2.4'  \
    --toplabel "$toplabel" \
    --plotname L1Mu_ResponseVsPt \
    --axisranges 0 100 0 1.6

# Response vs Run Number

$makeresol \
    -i $filezmumu \
    --h2d h_ResponseVsRunNb_AllQual_plots_eta0p0to0p83 h_ResponseVsRunNb_AllQual_plots_eta0p83to1p24 h_ResponseVsRunNb_AllQual_plots_eta1p24to2p4  \
    --xtitle 'run number' \
    --ytitle '(p_{T}^{L1Mu}/p_{T}^{reco muon})' \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{All qual.}' \
    --legend '0 #leq |#eta| < 0.83' '0.83 #leq |#eta| < 1.24' '1.24 #leq |#eta| < 2.4'  \
    --toplabel "$toplabel" \
    --axisrange 355374 362760 0 2 \
    --plotname L1Mu_ResponseVsRunNb
