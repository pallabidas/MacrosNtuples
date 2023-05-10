#!/bin/bash
# make_mu_comparisons.sh, draw L1Studies comparisons plots from histos obtained with ZToMuMu skim

# CL arguments
dir=$1
dir_A=$2
dir_B=$3
suffix_A=$4
suffix_B=$5

# some aliases (the drawplot.py must be in the same directory as the script, otherwise modify the path)
makeeff="python3 $PWD/drawplots.py -t efficiency --saveplot True"
makeresol="python3 $PWD/drawplots.py -t resolvsx --saveplot True"

# files
filezmumu_A=$PWD/$dir_A/all_ZToMuMu.root
filezmumu_B=$PWD/$dir_B/all_ZToMuMu.root

# move to workdir
cd $dir

for range in "EMTF" "BMTF" "OMTF"
do
    case $range in
        "EMTF")
            eta_range="eta1p24to2p4"
            eta_label='1.24 #leq |#eta^{#mu}(reco)| < 2.4'
            ;;

        "BMTF")
            eta_range="eta0p0to0p83"
            eta_label='0 #leq |#eta^{#mu}(reco)| < 0.83'
            ;;

        "OMTF")
            eta_range="eta0p83to1p24"
            eta_label='0.83 #leq |#eta^{#mu}(reco)| < 1.24'
            ;;

        *)
            ;;
    esac

    # Response vs Offline Pt

    $makeresol \
        -i $filezmumu_A $filezmumu_B \
        --h2d h_ResponseVsPt_AllQual_plots_"$eta_range" \
        --xtitle 'p_{T}^{reco muon} (GeV)' \
        --ytitle '(p_{T}^{L1Mu}/p_{T}^{reco muon})' \
        --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}{$eta_label}" \
        --legend '' \
        --axisranges 0 100 0 1.6  \
        --plotname L1Mu_ResponseVsPt_"$range" \
        --suffix_files "$suffix_A" "$suffix_B"

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
                qual_label='All qual.'
                ;;

            *)
                ;;
        esac

        # Efficiency vs pT (pT>22)
        # all eta ranges and all qualities

        $makeeff -i $filezmumu_A $filezmumu_B \
            --den h_"$Qual"_plots_"$eta_range" \
            --num h_"$Qual"_plots_"$eta_range"_l1thrgeq22 \
            --xtitle 'p_{T}^{#mu}(reco) (GeV)' \
            --ytitle "Efficiency" \
            --legend '' \
            --axisranges 3 500 \
            --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}{#splitline{$eta_label}{p_{T}^{L1 #mu} #geq 22 GeV}}" \
            --setlogx True \
            --plotname L1Mu22_TurnOn"$Qual"_"$range" \
            --suffix_files "$suffix_A" "$suffix_B"

        # Efficiency vs pT (pT>5)
        # all eta ranges and all qualities

        $makeeff -i $filezmumu_A $filezmumu_B \
            --den h_"$Qual"_plots_"$eta_range" \
            --num h_"$Qual"_plots_"$eta_range"_l1thrgeq5 \
            --xtitle 'p_{T}^{#mu}(reco) (GeV)' \
            --ytitle "Efficiency" \
            --legend '' \
            --axisranges 3 500 \
            --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}{#splitline{$eta_label}{p_{T}^{L1 #mu} #geq 5 GeV}}" \
            --setlogx True \
            --plotname L1Mu5_TurnOn"$Qual"_"$range" \
            --suffix_files "$suffix_A" "$suffix_B"

        # same thing, zoom on the 0 - 50 GeV region in pT

        # pT > 22
        $makeeff -i $filezmumu_A $filezmumu_B \
            --den h_"$Qual"_plots_"$eta_range" \
            --num h_"$Qual"_plots_"$eta_range"_l1thrgeq22 \
            --xtitle 'p_{T}^{#mu}(reco) (GeV)' \
            --ytitle "Efficiency" \
            --legend '' \
            --axisranges 3 50 \
            --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}{#splitline{$eta_label}{p_{T}^{L1 #mu} #geq 22 GeV}}" \
            --setlogx True \
            --plotname L1Mu22_TurnOn"$Qual"_"$range"_Zoom \
            --suffix_files "$suffix_A" "$suffix_B"

        # pT > 5
        $makeeff -i $filezmumu_A $filezmumu_B \
            --den h_"$Qual"_plots_"$eta_range" \
            --num h_"$Qual"_plots_"$eta_range"_l1thrgeq5 \
            --xtitle 'p_{T}^{#mu}(reco) (GeV)' \
            --ytitle "Efficiency" \
            --legend '' \
            --axisranges 3 50 \
            --extralabel "#splitline{Z#rightarrow#mu#mu, $qual_label}{#splitline{$eta_label}{p_{T}^{L1 #mu} #geq 5 GeV}}" \
            --setlogx True \
            --plotname L1Mu5_TurnOn"$Qual"_"$range"_Zoom \
            --suffix_files "$suffix_A" "$suffix_B"
    done
done

# Prefiring vs Eta only

$makeeff -i $filezmumu_A $filezmumu_B \
    --num L1Mu10to21_bxmin1_eta  \
    --den L1Mu10to21_bx0_eta  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle 'bx-1 / (bx0 or bx-1)' \
    --legend '' \
    --legendpos "top" \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual. #geq 12}' \
    --plotname L1Mu_PrefiringvsEta \
    --axisranges -2.5 2.5 0 0.1 \
    --addnumtoden True \
    --suffix_files "$suffix_A" "$suffix_B"

# Postfiring vs Eta only

$makeeff -i $filezmumu_A $filezmumu_B \
    --num L1Mu10to21_bxplus1_eta  \
    --den L1Mu10to21_bx0_eta  \
    --xtitle '#eta^{#mu}(reco)' \
    --ytitle 'bx+1 / (bx0 or bx+1)' \
    --legend '' \
    --legendpos "top" \
    --extralabel '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual. #geq 12}' \
    --plotname L1Mu_PostfiringvsEta \
    --axisranges -2.5 2.5 0 0.1 \
    --addnumtoden True \
    --suffix_files "$suffix_A" "$suffix_B"
