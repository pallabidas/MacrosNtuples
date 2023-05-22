#!/bin/bash


for run in '2023B' '2023C'
do
    for skim in 'Muon','ZToMuMu' 'Muon','MuonJet' 'EGamma','ZToEE' 'EGamma','PhotonJet'
    do
        IFS=','
        set $skim
        dir=/pnfs/iihe/cms/ph/sc4/store/data/Run$run/$1?/NANOAOD/PromptNanoAODv11p9_v1-v?

        echo $run $2
        sh SubmitToCondor_nano.sh outdir/"$run"/outputcondor_"$2" "$2" "$dir/*/*.root"
    done
done
