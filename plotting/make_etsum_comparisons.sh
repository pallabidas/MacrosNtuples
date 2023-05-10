#!/bin/bash
# make_etsum_comparisons.sh, draw L1Studies comparisons plots from MET histos obtained with MuonJet skim

# CL arguments
dir=$1
dir_A=$2
dir_B=$3
suffix_A=$4
suffix_B=$5

# some aliases (the drawplot.py must be in the same directory as the script, otherwise modify the path)
makeeff="python3 $PWD/drawplots.py -t efficiency --saveplot True"

# files
filemujet_A=$PWD/$dir_A/all_MuonJet.root
filemujet_B=$PWD/$dir_B/all_MuonJet.root

# move to workdir
cd $dir

# set some labels
extralabel='#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#splitline{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5)}{' # }}'

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight \
    --den h_MetNoMu_Denominator \
    --legend '' \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel PFMHTNoMu120}}" \
    --axisranges 0. 400. \
    --plotname L1ETSum_FromSingleMuon_HLTMET120_TurnOn_Zoom \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight   \
    --den h_MetNoMu_Denominator \
    --legend '' \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel PFMHTNoMu120}}" \
    --axisranges 0. 2000. \
    --plotname L1ETSum_FromSingleMuon_HLTMET120_TurnOn \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HLT_PFHT1050   \
    --den h_HT_Denominator \
    --legend '' \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T} > 30 GeV, 0 #leq |#eta| < 2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel PFHT1050}}" \
    --plotname L1ETSum_FromSingleMuon_HLT1050_TurnOn \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_MetNoMu_ETMHF80 \
    --den h_MetNoMu_Denominator \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel ETMHF80}}" \
    --axisranges 0. 2000. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_ETMHF80_TurnOn \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_MetNoMu_ETMHF80 \
    --den h_MetNoMu_Denominator \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel ETMHF80}}" \
    --axisranges 0. 400. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_ETMHF80_TurnOn_Zoom \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_MetNoMu_ETMHF100 \
    --den h_MetNoMu_Denominator \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel ETMHF100}}" \
    --axisranges 0. 2000. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_ETMHF100_TurnOn \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_MetNoMu_ETMHF100 \
    --den h_MetNoMu_Denominator \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel ETMHF100}}" \
    --axisranges 0. 400. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_ETMHF100_TurnOn_Zoom \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HT_L1_HTT200er \
    --den h_HT_Denominator \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel HTT200er}}" \
    --axisranges 0. 3000. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_HTT200_TurnOn \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HT_L1_HTT200er \
    --den h_HT_Denominator \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel HTT200er}}" \
    --axisranges 0. 1000. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_HTT200_TurnOn_Zoom \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HT_L1_HTT280er \
    --den h_HT_Denominator \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel HTT280er}}" \
    --axisranges 0. 3000. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_HTT280_TurnOn \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HT_L1_HTT280er \
    --den h_HT_Denominator \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel HTT280er}}" \
    --axisranges 0. 1000. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_HTT280_TurnOn_Zoom \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HT_L1_HTT360er \
    --den h_HT_Denominator \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel HTT360er}}" \
    --axisranges 0. 3000. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_HTT360_TurnOn \
    --suffix_files "$suffix_A" "$suffix_B"

$makeeff \
    -i $filemujet_A $filemujet_B \
    --num h_HT_L1_HTT360er \
    --den h_HT_Denominator \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel HTT360er}}" \
    --axisranges 0. 1000. \
    --legend '' \
    --plotname L1ETSum_FromSingleMuon_HTT360_TurnOn_Zoom \
    --suffix_files "$suffix_A" "$suffix_B"
