#!/bin/bash

for run in '2023B' '2023C'
do
    for skim in 'Muon','ZToMuMu' 'Muon','MuonJet' 'EGamma','ZToEE' 'EGamma','PhotonJet'
    do
        IFS=','
        set $skim
        case $run in
            "2023B")
                dir=/pnfs/iihe/cms/ph/sc4/store/data/Run$run/$1?/NANOAOD/PromptNanoAODv11p9_v1-v?
                golden='Cert_Collisions2023_eraB_366403_367079_Golden.json'
                ;;

            "2023C")
                dir=/pnfs/iihe/cms/ph/sc4/store/data/Run$run/$1?/NANOAOD/PromptNanoAODv12_v[2-4]-v?
                golden='Cert_Collisions2023_eraC_367095_368224_Golden.json'
                ;;

            *)
                dir=''
                golden=''
                ;;
        esac


        echo $run $2
        sh SubmitToCondor_nano.sh outdir/"$run"/outputcondor_"$2" "$2" "$dir/*/*.root"
        sh SubmitToCondor_nano.sh outdir/golden_"$run"/outputcondor_"$2" "$2" "$dir/*/*.root" $golden
    done
done
