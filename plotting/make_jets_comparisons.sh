#!/bin/bash
# make_jets_comparisons.sh, draw L1Studies comparisons plots from histos obtained with the MuonJet and PhotonJet skims

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
filemujet_A=$PWD/$dir_A/all_MuonJet.root
filemujet_B=$PWD/$dir_B/all_MuonJet.root
filegamjet_A=$PWD/$dir_A/all_PhotonJet.root
filegamjet_B=$PWD/$dir_B/all_PhotonJet.root

if [ dir_A == '2022RunGv1' ]
then
    filemujet_A=$PWD/others/2022RunGv1_PUPPI/all_MuonJet.root
fi

# set some labels
muselection='#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24'
photonselection='#geq 1 tight #gamma (p_{T} > 115 GeV, |#eta| < 1.479)'

cd $dir

for skim in "FromEGamma" "FromSingleMuon"
do

    case $skim in 
        "FromSingleMuon")
            selection_label=$muselection
            file_A=$filemujet_A
            file_B=$filemujet_B
            ;;
        "FromEGamma")
            selection_label=$photonselection
            file_A=$filegamjet_A
            file_B=$filegamjet_B
            ;;
        *)
            ;;
    esac

    for range in "barrel" "endcap1" "endcap2" "hf1" 
    do
        case $range in 
            "barrel")
                eta_range="eta0p0to1p3"
                mujet_label='#splitline{>=1 tight muon (p_{T}>27 GeV), pass HLT_IsoMu24}{#color[4]{0<=|#eta^{jet}(reco)|<1.3}}'
                gammajet_label='#splitline{>=1 tight photon (p_{T}>115 GeV, |#eta|<1.479), PFMET<50 GeV}{#color[4]{0.0<=|#eta^{jet}(reco)|<1.3}}' \
                pt_max=2000
                ;;

            "endcap1")
                eta_range="eta1p3to2p5"
                mujet_label='#splitline{>=1 tight muon (p_{T}>27 GeV), pass HLT_IsoMu24}{#color[4]{1.3<=|#eta^{jet}(reco)|<2.5}}'
                gammajet_label='#splitline{>=1 tight photon (p_{T}>115 GeV, |#eta|<1.479), PFMET<50 GeV}{#color[4]{1.3<=|#eta^{jet}(reco)|<2.5}}' \
                pt_max=1000
                ;;

            "endcap2")
                eta_range="eta2p5to3p0"
                mujet_label='#splitline{>=1 tight muon (p_{T}>27 GeV), pass HLT_IsoMu24}{#color[4]{2.5<=|#eta^{jet}(reco)|<3.0}}'
                gammajet_label='#splitline{>=1 tight photon (p_{T}>115 GeV, |#eta|<1.479), PFMET<50 GeV}{#color[4]{2.5<=|#eta^{jet}(reco)|<3.0}}' \
                pt_max=500
                ;;

            "hf1")
                eta_range="eta3p0to3p5"
                mujet_label='#splitline{>=1 tight muon (p_{T}>27 GeV), pass HLT_IsoMu24}{#color[4]{3.0<=|#eta^{jet}(reco)|<3.5}}'
                gammajet_label='#splitline{>=1 tight photon (p_{T}>115 GeV, |#eta|<1.479), PFMET<50 GeV}{#color[4]{3.0<=|#eta^{jet}(reco)|<3.5}}' \
                pt_max=500
                ;;

            *)
                eta_range=""
                mujet_label=""
                gammajet_label=""
                pt_max=2000
                ;;
        esac
    done

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

        # Response vs Offline Pt

        $makeresol \
            -i $file_A $file_B \
            --h2d h_ResponseVsPt_Jet_plots_"$eta_range" \
            --xtitle 'p_{T}^{reco jet} (GeV)' \
            --ytitle '(p_{T}^{L1 jet}/p_{T}^{reco jet})' \
            --extralabel "#splitline{$selection_label}{p_{T}^{jet} > 30 GeV, $eta_label}" \
            --legend '' \
            --legendpos 'top' \
            --axisrange 0 200 0 1.6 \
            --plotname L1Jet_"$skim"_ResponseVsPt_"$range" \
            --suffix_files "$suffix_A" "$suffix_B"

        # Efficiency vs pT (pT>40)
        # all eta ranges and all qualities

        $makeeff -i $file_A $file_B \
            --den h_Jet_plots_"$eta_range" \
            --num h_Jet_plots_"$eta_range"_l1thrgeq40p0 \
            --xtitle 'p_{T}^{jet}(reco) (GeV)' \
            --ytitle 'Efficiency' \
            --legend '' \
            --axisranges 30 $pt_max \
            $logx \
            --extralabel "#splitline{$selection_label}{#splitline{p_{T}^{jet} > 30 GeV, $eta_label}{p_{T}^{L1 jet} #geq 40 GeV}}" \
            --plotname L1Jet40_"$skim"_TurnOn_"$range" \
            --suffix_files "$suffix_A" "$suffix_B"

        # Efficiency vs pT (pT>180)
        # all eta ranges and all qualities

        $makeeff -i $file_A $file_B \
            --den h_Jet_plots_"$eta_range" \
            --num h_Jet_plots_"$eta_range"_l1thrgeq180p0 \
            --xtitle 'p_{T}^{jet}(reco) (GeV)' \
            --ytitle 'Efficiency' \
            --legend '' \
            --axisranges 30 $pt_max \
            $logx \
            --extralabel "#splitline{$selection_label}{#splitline{p_{T}^{jet} > 30 GeV, $eta_label}{p_{T}^{L1 jet} #geq 180 GeV}}" \
            --plotname L1Jet180_"$skim"_TurnOn_"$range" \
            --suffix_files "$suffix_A" "$suffix_B"

        # same thing, zoom on the 0 - 300 GeV region in pT

        # Efficiency vs pT (pT>40)
        # all eta ranges and all qualities

        $makeeff -i $file_A $file_B \
            --den h_Jet_plots_"$eta_range" \
            --num h_Jet_plots_"$eta_range"_l1thrgeq40p0 \
            --xtitle 'p_{T}^{jet}(reco) (GeV)' \
            --ytitle 'Efficiency' \
            --legend '' \
            --axisranges 30 500 \
            --extralabel "#splitline{$selection_label}{#splitline{p_{T}^{jet} > 30 GeV, $eta_label}{p_{T}^{L1 jet} #geq 40 GeV}}" \
            --plotname L1Jet40_"$skim"_TurnOn_"$range"_Zoom \
            --suffix_files "$suffix_A" "$suffix_B"

        # Efficiency vs pT (pT>180)
        # all eta ranges and all qualities

        $makeeff -i $file_A $file_B \
            --den h_Jet_plots_"$eta_range" \
            --num h_Jet_plots_"$eta_range"_l1thrgeq180p0 \
            --xtitle 'p_{T}^{jet}(reco) (GeV)' \
            --ytitle 'Efficiency' \
            --legend '' \
            --axisranges 30 500 \
            --extralabel "#splitline{$selection_label}{#splitline{p_{T}^{jet} > 30 GeV, $eta_label}{p_{T}^{L1 jet} #geq 180 GeV}}" \
            --plotname L1Jet180_"$skim"_TurnOn_"$range"_Zoom \
            --suffix_files "$suffix_A" "$suffix_B"

    done

    # Prefiring vs Eta only

    $makeeff -i $file_A $file_B \
        --num L1Jet100to150_bxmin1_eta  \
        --den L1Jet100to150_bx0_eta  \
        --xtitle '#eta^{jet}(reco)' \
        --ytitle 'bx-1 / (bx0 or bx-1)' \
        --legend '' \
        --legendpos 'top' \
        --extralabel "#splitline{$selection_label}{p_{T}^{jet} > 30 GeV}" \
        --plotname  L1Jet_"$skim"_PrefiringvsEta \
        --axisranges -5 5 0 1.1 \
        --addnumtoden True \
        --suffix_files "$suffix_A" "$suffix_B"

    # Postfiring vs Eta only

    $makeeff -i $file_A $file_B \
        --num L1Jet100to150_bxplus1_eta  \
        --den L1Jet100to150_bx0_eta  \
        --xtitle '#eta^{jet}(reco)' \
        --ytitle 'bx+1 / (bx0 or bx+1)' \
        --legend '' \
        --legendpos 'top' \
        --extralabel "#splitline{$selection_label}{p_{T}^{jet} > 30 GeV}" \
        --plotname  L1Jet_"$skim"_PostfiringvsEta \
        --axisranges -5 5 0 1.1 \
        --addnumtoden True \
        --suffix_files "$suffix_A" "$suffix_B"
done
