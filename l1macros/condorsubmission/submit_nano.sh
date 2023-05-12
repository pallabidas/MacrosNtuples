#!/bin/bash

echo 2023B ZToMuMu
sh SubmitToCondor.sh outdir/2023B/outputcondor_ZToMuMu ZToMuMu "/user/hevard/CMSSW_12_4_8/src/MacrosNtuples/l1macros/test_io/Run2023B/Muons/*.root"
echo 2023B MuonJet
sh SubmitToCondor.sh outdir/2023B/outputcondor_MuonJet MuonJet "/user/hevard/CMSSW_12_4_8/src/MacrosNtuples/l1macros/test_io/Run2023B/Muons/*.root"
echo 2023B ZToEE
sh SubmitToCondor.sh outdir/2023B/outputcondor_ZToEE ZToEE "/pnfs/iihe/cms/ph/sc4/store/data/Run2023B/EGamma*/NANOAOD/PromptNanoAODv11p9_v1-v1/*/*.root"
echo 2023B PhotonJet
sh SubmitToCondor.sh outdir/2023B/outputcondor_PhotonJet PhotonJet "/pnfs/iihe/cms/ph/sc4/store/data/Run2023B/EGamma*/NANOAOD/PromptNanoAODv11p9_v1-v1/*/*.root"
