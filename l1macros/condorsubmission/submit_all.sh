#!/bin/bash

for run in 'C1' 'D1' 'D2' 'E1' 'F1' 'G1'
#for run in 'C1' 'D1' 'D2' 'E1' 'F1' 
#for run in 'G1'
do
    for skim in "Muon","ZToMuMu" "Muon","SingleMuforJME" "EGamma","ZToEE" "EGamma","SinglePhotonforJME"
    #for skim in "Muon","ZToMuMu" 
    do 
        IFS=","
        set $skim
        #dir=`ls -d1 /pnfs/iihe/cms/store/user/hevard/$1/Run2022${run:0:1}_PromptReco_v${run:1:1}_DataRun3_L1Study_$2/22* | tail -n 1`
        #dir=`ls -d1 /pnfs/iihe/cms/store/user/hevard/$1/Run2022${run:0:1}_PromptReco_v${run:1:1}_DataRun3_L1Study_$2/* | tail -n 1`
        #dir=`ls -d1 /pnfs/iihe/cms/store/user/hevard/$1/Run2022${run:0:1}_PromptReco_v${run:1:1}_DataRun3_L1Study_$2/* | tail -n 2 | head -n 1`
        dir=`ls -d1 /pnfs/iihe/cms/store/user/hevard/$1/Run2022${run:0:1}_PromptReco_v${run:1:1}_DataRun3_L1Study_$2/230329* | tail -n 1`

        case $2 in
            "ZToMuMu")
                condor_skim="ZToMuMu"
                ;;

            "SingleMuforJME")
                condor_skim="MuonJet"
                ;;

            "ZToEE")
                condor_skim="ZToEE"
                ;;

            "SinglePhotonforJME")
                condor_skim="PhotonJet"
                ;;
        esac

        outdir="2022Run${run:0:1}v${run:1:1}"

        echo $outdir $condor_skim
        sh SubmitToCondor.sh outdir/"$outdir"/outputcondor_"$condor_skim" "$condor_skim" "$dir/*/*.root"
        #echo $dir

    done
done

# Begginning of 2022C

#sh SubmitToCondor.sh outdir/2022RunCv1_start/outputcondor_ZToMuMu ZToMuMu "/pnfs/iihe/cms/store/user/hevard/SingleMuon/Run2022C_PromptReco_v1_DataRun3_L1Study_ZToMuMu/221214_155554/*/*.root" 
#sh SubmitToCondor.sh outdir/2022RunCv1_start/outputcondor_MuonJet MuonJet "/pnfs/iihe/cms/store/user/hevard/SingleMuon/Run2022C_PromptReco_v1_DataRun3_L1Study_SingleMuforJME/221214_155734/*/*.root" 

echo 2022RunCv1_start ZToMuMu
sh SubmitToCondor.sh outdir/2022RunCv1_start/outputcondor_ZToMuMu ZToMuMu "/pnfs/iihe/cms/store/user/hevard/SingleMuon/Run2022C_PromptReco_v1_DataRun3_L1Study_ZToMuMu/230329_095441/*/*.root" 
echo 2022RunCv1_start MuonJet
sh SubmitToCondor.sh outdir/2022RunCv1_start/outputcondor_MuonJet MuonJet "/pnfs/iihe/cms/store/user/hevard/SingleMuon/Run2022C_PromptReco_v1_DataRun3_L1Study_SingleMuforJME/230329_095517/*/*.root" 


# 2018D

#sh SubmitToCondor.sh outdir/2018D/outputcondor_MuonJet MuonJet /pnfs/iihe/cms/store/user/lathomas/SingleMuon/Run2018D_UL2018_MiniAODv2_v3_DataUL2018D_L1Study_SingleMuforJME/220923_115303/0000/\*.root
#sh SubmitToCondor.sh outdir/2018D/outputcondor_ZToMuMu ZToMuMu /pnfs/iihe/cms/store/user/lathomas/SingleMuon/Run2018D_UL2018_MiniAODv2_v3_DataUL2018D_L1Study_ZToMuMu/220923_114505/0000/\*.root
#sh SubmitToCondor.sh outdir/2018D/outputcondor_ZToEE ZToEE /pnfs/iihe/cms/store/user/lathomas/EGamma/Run2018D_UL2018_MiniAODv2_v2_DataRun3_L1Study_ZToEE/220913_203229/000\*/\*.root
#sh SubmitToCondor.sh outdir/2018D/outputcondor_PhotonJet PhotonJet /pnfs/iihe/cms/store/user/lathomas/EGamma/Run2018D_UL2018_MiniAODv2_v2_DataUL2018D_L1Study_SinglePhotonforJME/220923_120114/000\*/\*.root

echo 2018D ZToMuMu
sh SubmitToCondor.sh outdir/2018D/outputcondor_ZToMuMu ZToMuMu "/pnfs/iihe/cms/store/user/hevard/SingleMuon/Run2018D_UL2018_MiniAODv2_GT36_v1_DataUL2018D_L1Study_ZToMuMu/230329_120344/*/*.root"
echo 2018D MuonJet
sh SubmitToCondor.sh outdir/2018D/outputcondor_MuonJet MuonJet "/pnfs/iihe/cms/store/user/hevard/SingleMuon/Run2018D_UL2018_MiniAODv2_GT36_v1_DataUL2018D_L1Study_SingleMuforJME/230329_120422/*/*.root"
echo 2018D ZToEE
sh SubmitToCondor.sh outdir/2018D/outputcondor_ZToEE ZToEE "/pnfs/iihe/cms/store/user/hevard/EGamma/Run2018D_UL2018_MiniAODv2_v2_DataUL2018D_L1Study_ZToEE/230329_120501/*/*.root"
echo 2018D PhotonJet
sh SubmitToCondor.sh outdir/2018D/outputcondor_PhotonJet PhotonJet "/pnfs/iihe/cms/store/user/hevard/EGamma/Run2018D_UL2018_MiniAODv2_v2_DataUL2018D_L1Study_SinglePhotonforJME/230329_120539/*/*.root"
