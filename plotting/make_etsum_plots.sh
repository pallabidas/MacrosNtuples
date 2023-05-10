# make_etsum_plots.sh, draw L1Studies plots from MET histos obtained with the MuonJet skim

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

# move to workdir
cd $dir
filemujet=all_MuonJet.root

# set some labels
toplabel="#sqrt{s} = 13.6 TeV, L_{int} = $lumi fb^{-1}"
#toplabel="$lumi"

extralabel='#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5)}'

if [ -z "$nvtx_suffix" ]
then
    $makeeff \
        -i $filemujet \
        --num h_MetNoMu_ETMHF100_nvtx10to20 h_MetNoMu_ETMHF100_nvtx20to30 h_MetNoMu_ETMHF100_nvtx30to40 h_MetNoMu_ETMHF100_nvtx40to50 h_MetNoMu_ETMHF100_nvtx50to60 \
        --den h_MetNoMu_Denominator_nvtx10to20 h_MetNoMu_Denominator_nvtx20to30 h_MetNoMu_Denominator_nvtx30to40 h_MetNoMu_Denominator_nvtx40to50 h_MetNoMu_Denominator_nvtx50to60 \
        --xtitle 'PFMET(#mu subtracted) (GeV)' \
        --ytitle 'Efficiency'  \
        --extralabel '#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#splitline{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5)}{ETMHF100}}' \
        --axisranges 0. 2000. \
        --legend 'nvtx #in #[]{10, 20}' 'nvtx #in #[]{20, 30}' 'nvtx #in #[]{30, 40}' 'nvtx #in #[]{40, 50}' 'nvtx #in #[]{50, 60}' \
        --toplabel "$toplabel" \
        --plotname L1ETSum_FromSingleMuon_ETMHF100_TurnOn_vsPU

    $makeeff \
        -i $filemujet \
        --num h_MetNoMu_ETMHF100_nvtx10to20 h_MetNoMu_ETMHF100_nvtx20to30 h_MetNoMu_ETMHF100_nvtx30to40 h_MetNoMu_ETMHF100_nvtx40to50 h_MetNoMu_ETMHF100_nvtx50to60 \
        --den h_MetNoMu_Denominator_nvtx10to20 h_MetNoMu_Denominator_nvtx20to30 h_MetNoMu_Denominator_nvtx30to40 h_MetNoMu_Denominator_nvtx40to50 h_MetNoMu_Denominator_nvtx50to60 \
        --xtitle 'PFMET(#mu subtracted) (GeV)' \
        --ytitle 'Efficiency'  \
        --extralabel '#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#splitline{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5)}{ETMHF100}}' \
        --axisranges 0. 400. \
        --legend 'nvtx #in #[]{10, 20}' 'nvtx #in #[]{20, 30}' 'nvtx #in #[]{30, 40}' 'nvtx #in #[]{40, 50}' 'nvtx #in #[]{50, 60}' \
        --toplabel "$toplabel" \
        --plotname L1ETSum_FromSingleMuon_ETMHF100_TurnOn_vsPU_Zoom

    $makeeff \
        -i $filemujet \
        --num h_HT_L1_HTT360er_nvtx10to20 h_HT_L1_HTT360er_nvtx20to30 h_HT_L1_HTT360er_nvtx30to40 h_HT_L1_HTT360er_nvtx40to50 h_HT_L1_HTT360er_nvtx50to60 \
        --den h_HT_Denominator_nvtx10to20 h_HT_Denominator_nvtx20to30 h_HT_Denominator_nvtx30to40 h_HT_Denominator_nvtx40to50 h_HT_Denominator_nvtx50to60 \
        --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
        --ytitle 'Efficiency'  \
        --extralabel '#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#splitline{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5)}{HTT360er}}' \
        --axisranges 0. 3000. \
        --legend 'nvtx #in #[]{10, 20}' 'nvtx #in #[]{20, 30}' 'nvtx #in #[]{30, 40}' 'nvtx #in #[]{40, 50}' 'nvtx #in #[]{50, 60}' \
        --toplabel "$toplabel" \
        --plotname L1ETSum_FromSingleMuon_HTT360_TurnOn_vsPU

    $makeeff \
        -i $filemujet \
        --num h_HT_L1_HTT360er_nvtx10to20 h_HT_L1_HTT360er_nvtx20to30 h_HT_L1_HTT360er_nvtx30to40 h_HT_L1_HTT360er_nvtx40to50 h_HT_L1_HTT360er_nvtx50to60 \
        --den h_HT_Denominator_nvtx10to20 h_HT_Denominator_nvtx20to30 h_HT_Denominator_nvtx30to40 h_HT_Denominator_nvtx40to50 h_HT_Denominator_nvtx50to60 \
        --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
        --ytitle 'Efficiency'  \
        --extralabel '#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#splitline{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5)}{HTT360er}}' \
        --axisranges 0. 1000. \
        --legend 'nvtx #in #[]{10, 20}' 'nvtx #in #[]{20, 30}' 'nvtx #in #[]{30, 40}' 'nvtx #in #[]{40, 50}' 'nvtx #in #[]{50, 60}' \
        --toplabel "$toplabel" \
        --plotname L1ETSum_FromSingleMuon_HTT360_TurnOn_vsPU_Zoom
fi

$makeeff \
    -i $filemujet \
    --num h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight \
    --den h_MetNoMu_Denominator \
    --legend 'PFMHTNoMu120' \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel" \
    --axisranges 0. 400. \
    --toplabel "$toplabel" \
    --plotname L1ETSum_FromSingleMuon_HLTMET120_TurnOn_Zoom 

$makeeff \
    -i $filemujet \
    --num h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight   \
    --den h_MetNoMu_Denominator \
    --legend 'PFMHTNoMu120' \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel" \
    --axisranges 0. 2000. \
    --toplabel "$toplabel" \
    --plotname L1ETSum_FromSingleMuon_HLTMET120_TurnOn 

$makeeff \
    -i $filemujet \
    --num h_HLT_PFHT1050   \
    --den h_HT_Denominator \
    --legend 'PFHT1050' \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel" \
    --toplabel "$toplabel" \
    --plotname L1ETSum_FromSingleMuon_HLT1050_TurnOn 

$makeeff \
    -i $filemujet \
    --num h_MetNoMu_ETMHF80 h_MetNoMu_ETMHF100   \
    --den h_MetNoMu_Denominator \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel" \
    --axisranges 0. 400. \
    --legend 'ETMHF80' 'ETMHF100' \
    --toplabel "$toplabel" \
    --plotname L1ETSum_FromSingleMuon_ETMHF_TurnOn_Zoom 

$makeeff \
    -i $filemujet \
    --num h_MetNoMu_ETMHF80 h_MetNoMu_ETMHF100   \
    --den h_MetNoMu_Denominator \
    --xtitle 'PFMET(#mu subtracted) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel" \
    --axisranges 0. 2000. \
    --legend 'ETMHF80' 'ETMHF100' \
    --toplabel "$toplabel" \
    --plotname L1ETSum_FromSingleMuon_ETMHF_TurnOn 

$makeeff \
    -i $filemujet \
    --num h_HT_L1_HTT200er h_HT_L1_HTT280er h_HT_L1_HTT360er   \
    --den h_HT_Denominator \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel" \
    --axisranges 0. 1000. \
    --legend 'HTT200er' 'HTT280er' 'HTT360er' \
    --toplabel "$toplabel" \
    --plotname L1ETSum_FromSingleMuon_HTT_TurnOn_Zoom 

$makeeff \
    -i $filemujet \
    --num h_HT_L1_HTT200er h_HT_L1_HTT280er h_HT_L1_HTT360er   \
    --den h_HT_Denominator \
    --xtitle 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)' \
    --ytitle 'Efficiency'  \
    --extralabel "$extralabel" \
    --axisranges 0. 3000. \
    --legend 'HTT200er' 'HTT280er' 'HTT360er' \
    --toplabel "$toplabel" \
    --plotname L1ETSum_FromSingleMuon_HTT_TurnOn 
