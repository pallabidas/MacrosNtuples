#!/bin/bash
# make_mu_comparisons.sh, draw L1Studies comparisons plots from histos obtained with ZToEE skim

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
filezee_A=$PWD/$dir_A/all_ZToEE.root
filezee_B=$PWD/$dir_B/all_ZToEE.root

# move to workdir
cd $dir

for range in "barrel" "endcap"
do
    case $range in 
        "barrel")
            eta_range="eta0p0to1p479"
            eta_label='0.0 #leq |#eta^{e}(reco)| < 1.479'
            label='#splitline{Z#rightarrowee}{0<=|#eta^{e}(reco)|<1.479}' 
            ;;

        "endcap")
            eta_range="eta1p479to2p5"
            eta_label='1.479 #leq |#eta^{e}(reco)| < 2.5'
            label='#splitline{Z#rightarrowee}{1.479<=|#eta^{e}(reco)|<2.5}'
            ;;
        *)
            ;;
    esac

    # Response vs Offline Pt

    $makeresol \
        -i $filezee_A $filezee_B \
        --h2d h_ResponseVsPt_EGNonIso_plots_"$eta_range" \
        --xtitle 'p_{T}^{reco e} (GeV)' \
        --ytitle '(p_{T}^{L1EG}/p_{T}^{reco e})' \
        --extralabel "#splitline{Z#rightarrowee, Non Iso.}{$eta_label}" \
        --legend '' \
        --legendpos 'top' \
        --axisranges 0 100 0 1.6  \
        --plotname L1EGNonIso_ResponseVsPt_"$range" \
        --suffix_files "$suffix_A" "$suffix_B"

    for reco in "NonIso" "LooseIso" "TightIso"
    do

        # Efficiency vs pT (pT>10)
        # all eta ranges and all qualities

        $makeeff -i $filezee_A $filezee_B \
            --den h_EG"$reco"_plots_"$eta_range" \
            --num h_EG"$reco"_plots_"$eta_range"_l1thrgeq10 \
            --xtitle 'p_{T}^{e}(reco) (GeV)' \
            --ytitle "Efficiency" \
            --legend '' \
            --extralabel "#splitline{Z#rightarrowee, $reco}{#splitline{$eta_label}{p_{T}^{L1 e} #geq 10 GeV}}" \
            --setlogx True \
            --plotname L1EG10_TurnOn"$reco"_"$range" \
            --suffix_files "$suffix_A" "$suffix_B"

        # Efficiency vs pT (pT>36)
        # all eta ranges and all qualities

        $makeeff -i $filezee_A $filezee_B \
            --den h_EG"$reco"_plots_"$eta_range" \
            --num h_EG"$reco"_plots_"$eta_range"_l1thrgeq36 \
            --xtitle 'p_{T}^{e}(reco) (GeV)' \
            --ytitle "Efficiency" \
            --legend '' \
            --extralabel "#splitline{Z#rightarrowee, $reco}{#splitline{$eta_label}{p_{T}^{L1 e} #geq 36 GeV}}" \
            --setlogx True \
            --plotname L1EG36_TurnOn"$reco"_"$range" \
            --suffix_files "$suffix_A" "$suffix_B"

        # same thing, zoom on the 0 - 50 GeV region in pT

        # pT > 10
        $makeeff -i $filezee_A $filezee_B \
            --den h_EG"$reco"_plots_"$eta_range" \
            --num h_EG"$reco"_plots_"$eta_range"_l1thrgeq10 \
            --xtitle 'p_{T}^{e}(reco) (GeV)' \
            --ytitle "Efficiency" \
            --legend '' \
            --extralabel "#splitline{Z#rightarrowee, $reco}{#splitline{$eta_label}{p_{T}^{L1 e} #geq 10 GeV}}" \
            --setlogx True \
            --axisranges 10 50 \
            --plotname L1EG10_TurnOn"$reco"_"$range"_Zoom \
            --suffix_files "$suffix_A" "$suffix_B"

        # pT > 36
        $makeeff -i $filezee_A $filezee_B \
            --den h_EG"$reco"_plots_"$eta_range" \
            --num h_EG"$reco"_plots_"$eta_range"_l1thrgeq36 \
            --xtitle 'p_{T}^{e}(reco) (GeV)' \
            --ytitle "Efficiency" \
            --legend '' \
            --legendpos 'top' \
            --extralabel "#splitline{Z#rightarrowee, $reco}{#splitline{$eta_label}{p_{T}^{L1 e} #geq 36 GeV}}" \
            --setlogx True \
            --axisranges 10 50 \
            --plotname L1EG36_TurnOn"$reco"_"$range"_Zoom \
            --suffix_files "$suffix_A" "$suffix_B"
   done
done

# Prefiring vs Eta only

$makeeff -i $filezee_A $filezee_B \
    --num L1EG15to26_bxmin1_eta  \
    --den L1EG15to26_bx0_eta  \
    --xtitle '#eta^{e}(reco)' \
    --ytitle 'bx-1 / (bx0 or bx-1)' \
    --legend '' \
    --legendpos 'top' \
    --extralabel '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}' \
    --plotname L1EG_PrefiringvsEta \
    --axisranges -2.5 2.5 0 0.1 \
    --addnumtoden True \
    --suffix_files "$suffix_A" "$suffix_B"

# Postfiring vs Eta only

$makeeff -i $filezee_A $filezee_B \
    --num L1EG15to26_bxplus1_eta  \
    --den L1EG15to26_bx0_eta  \
    --xtitle '#eta^{e}(reco)' \
    --ytitle 'bx+1 / (bx0 or bx+1)' \
    --legend '' \
    --legendpos 'top' \
    --extralabel '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}' \
    --plotname L1EG_PostfiringvsEta \
    --axisranges -2.5 2.5 0 0.1 \
    --addnumtoden True \
    --suffix_files "$suffix_A" "$suffix_B"
