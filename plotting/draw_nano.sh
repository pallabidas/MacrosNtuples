#!/bin/bash

for dir in "2023B"
do
    python3 make_ZToMuMu_plots.py --dir $dir
    python3 make_ZToEE_plots.py --dir $dir
    python3 make_MuonJet_plots.py --dir $dir
    python3 make_PhotonJet_plots.py --dir $dir
done

