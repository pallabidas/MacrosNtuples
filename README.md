# MacrosNtuples
Macros to analyze flat ntuples such as NANOAOD ntuples, L1 ntuples or private ntuples

## Step-1: Make L1NTuple (no re-emulation, only unpacked TPs):
```
 cmsDriver.py l1Ntuple -s RAW2DIGI --python_filename=zmu.py -n -1 --no_output --era=Run3 --data --conditions=126X_dataRun3_Prompt_v2 --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleAODRAW --customise=L1Trigger/Configuration/customiseSettings.L1TSettingsToCaloParams_2022_v0_6  --filein=root://cms-xrd-global.cern.ch://store/data/Run2022F/Muon/RAW-RECO/ZMu-PromptReco-v1/000/361/971/00000/1af6642a-18c9-4f88-abfb-b1b441714a10.root
```

## Step-2 Follow MacrosNtuples/l1macros/README.md to make plots
