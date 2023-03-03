#!/bin/bash

cd /user/lathomas/L1Studies/SampleGeneration/SingleNeutrinoPU1/CMSSW_12_2_1/src
cmsenv 
cd /user/lathomas/PortingCodeToGitIIHECMS/CMSSW_12_4_8/src/MacrosNtuples/l1macros/

python3 performances.py --max_events -1 -i $1 -o $2 -c $3

